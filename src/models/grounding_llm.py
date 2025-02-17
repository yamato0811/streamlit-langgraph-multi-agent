import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerationResponse,
    GenerativeModel,
    Tool,
    grounding,
)


class GroundingLLM:
    def __init__(self):
        self.model_name = "gemini-1.5-flash"
        self.system_prompt = """
        あなたは高度な知識を持つAIアシスタントです。
        ユーザーの質問に対し、Google検索用のツールを利用して回答します。
        """
        self._initialize_vertexai()
        self.model = self._initialize_llm(self.model_name, self.system_prompt)
        self.tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())

    def _initialize_vertexai(self) -> None:
        vertexai.init()

    def _initialize_llm(self, model_name, system_prompt) -> GenerativeModel:
        return GenerativeModel(model_name=model_name, system_instruction=system_prompt)

    def __call__(self, user_prompt: str) -> GenerationResponse:
        response = self.model.generate_content(
            user_prompt,
            tools=[self.tool],
            generation_config=GenerationConfig(
                temperature=0.0,
            ),
        )
        return response

    def get_citations(self, response: GenerationResponse) -> str:
        urls = ""
        grounding_chunks = response.candidates[0].grounding_metadata.grounding_chunks
        for grounding_chunk in grounding_chunks:
            urls += f"- [{grounding_chunk.web.title}]({grounding_chunk.web.uri})\n"
        info_citations = f"#### 参考URL\n\n{urls}"
        return info_citations
