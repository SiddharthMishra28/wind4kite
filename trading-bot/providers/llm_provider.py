import os
import litellm
from typing import List, Dict, Any, Optional

class LLMProvider:
    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

        if api_key:
            os.environ[self._get_api_key_env_var()] = api_key
        if base_url:
            os.environ[self._get_base_url_env_var()] = base_url

    def _get_api_key_env_var(self) -> str:
        if "gpt" in self.model:
            return "OPENAI_API_KEY"
        elif "claude" in self.model:
            return "ANTHROPIC_API_KEY"
        elif "ollama" in self.model:
            return "OLLAMA_API_KEY"
        return "LLM_API_KEY"

    def _get_base_url_env_var(self) -> str:
        return "LLM_BASE_URL"

    def completion(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None) -> Any:
        try:
            response = litellm.completion(
                model=self.model,
                messages=messages,
                tools=tools,
                api_key=self.api_key,
                base_url=self.base_url
            )
            return response
        except Exception as e:
            print(f"Error in LLM completion: {e}")
            return None

    def get_cost(self, response: Any) -> float:
        if response is None:
            return 0.0
        return litellm.completion_cost(completion_response=response)
