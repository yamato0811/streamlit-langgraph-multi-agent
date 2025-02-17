import vertexai
from langchain_core.language_models import BaseChatModel
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_google_vertexai import ChatVertexAI


class LLM:
    def __init__(self, model_name: str, temperature: float):
        self.model = self._initialize_llm(model_name, temperature)

    def _initialize_llm(self, model_name: str, temperature: float) -> BaseChatModel:
        if model_name == "gemini":
            vertexai.init()
            return ChatVertexAI(model="gemini-2.0-flash", temperature=temperature)
        else:
            raise ValueError(f"Model name {model_name} not supported.")

    def __call__(self, input: LanguageModelInput) -> BaseMessage:
        """LLMの呼び出し"""
        try:
            return self.model.invoke(input)
        except Exception as e:
            raise e
