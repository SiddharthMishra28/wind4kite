import asyncio
import threading
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Optional, List, Any

class KiteMCPClient:
    def __init__(self, command: str = "npx", args: List[str] = ["mcp-remote", "https://mcp.kite.trade/mcp"]):
        self.server_params = StdioServerParameters(
            command=command,
            args=args,
            env=None
        )
        self.session: Optional[ClientSession] = None
        self._stdio_mgr = None

    async def connect(self):
        if self.session:
            return
        self._stdio_mgr = stdio_client(self.server_params)
        read, write = await self._stdio_mgr.__aenter__()
        self.session = ClientSession(read, write)
        await self.session.initialize()

    async def disconnect(self):
        if self._stdio_mgr:
            await self._stdio_mgr.__aexit__(None, None, None)
            self.session = None
            self._stdio_mgr = None

    async def list_tools(self):
        if not self.session:
            await self.connect()
        return await self.session.list_tools()

    async def call_tool(self, tool_name: str, arguments: dict):
        if not self.session:
            await self.connect()
        return await self.session.call_tool(tool_name, arguments)

class KiteMCPWrapper:
    """Thread-safe synchronous wrapper for KiteMCPClient."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(KiteMCPWrapper, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.client = KiteMCPClient()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()
        self._initialized = True

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _run_coro(self, coro):
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result()

    def connect(self):
        return self._run_coro(self.client.connect())

    def disconnect(self):
        return self._run_coro(self.client.disconnect())

    def get_holdings(self):
        return self._run_coro(self.client.call_tool("get_holdings", {}))

    def get_orders(self):
        return self._run_coro(self.client.call_tool("get_orders", {}))

    def place_order(self, **kwargs):
        return self._run_coro(self.client.call_tool("place_order", kwargs))

    def __del__(self):
        if hasattr(self, 'loop') and self.loop.is_running():
            self.disconnect()
            self.loop.call_soon_threadsafe(self.loop.stop)
