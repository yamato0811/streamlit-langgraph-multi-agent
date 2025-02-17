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

    def map_text_with_citations(self, response: dict) -> str:
        """
        テキストと参照情報をマッピングする関数
        """

        # メインテキストを取得
        text = response["candidates"][0]["content"]["parts"][0]["text"]

        # 参照情報を取得
        supports = response["candidates"][0]["grounding_metadata"]["grounding_supports"]
        chunks = response["candidates"][0]["grounding_metadata"]["grounding_chunks"]

        # HTMLの検索キーワードを取得
        entry_point_html = response["candidates"][0]["grounding_metadata"][
            "search_entry_point"
        ]["rendered_content"]

        # URLとインデックスのマッピングを作成
        url_map = {}
        for i, chunk in enumerate(chunks):
            if "web" in chunk and "uri" in chunk["web"]:
                url_map[i] = {
                    "url": chunk["web"]["uri"],
                    "title": chunk["web"]["title"],
                }

        # テキストを段落に分割
        paragraphs = text.split("\n\n")

        # 各段落に対して参照情報を付与
        processed_paragraphs = []
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue

            # この段落に対応するsupportsを探す
            relevant_supports = [
                support
                for support in supports
                if support["segment"]["text"] in paragraph
            ]

            if relevant_supports:
                # 参照情報を付与
                references = set()
                for support in relevant_supports:
                    for index in support["grounding_chunk_indices"]:
                        if index in url_map:
                            references.add(f"[{index}]")

                if references:
                    paragraph = f"{paragraph} {' '.join(sorted(references))}"

            processed_paragraphs.append(paragraph)

        # 参照リストを作成
        reference_list = []
        for index, info in sorted(url_map.items()):
            reference_list.append(f"* [{index}]：[{info['title']}]({info['url']})")

        # 最終的なテキストを組み立て
        final_text = "\n\n".join(processed_paragraphs)
        final_text += "\n\n#### 引用情報\n\n"
        final_text += "\n".join(reference_list)
        final_text += "\n\n#### 検索ワード\n\n"
        final_text += entry_point_html

        return final_text

    def include_citations(self, response: GenerationResponse) -> bool:
        if len(response.candidates[0].grounding_metadata.grounding_chunks) > 0:
            return True
        return False
