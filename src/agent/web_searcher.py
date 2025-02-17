from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from agent.state import AgentState
from models.grounding_llm import GroundingLLM


class WebSearcher:
    def __init__(self, grounding_llm: GroundingLLM) -> None:
        self.grounding_llm = grounding_llm
        self.graph = self.build_graph()

    def build_graph(self) -> CompiledStateGraph:
        graph_builder = StateGraph(AgentState)
        graph_builder.add_node(self.web_search)
        graph_builder.add_node(self.post_process)

        graph_builder.set_entry_point("web_search")
        graph_builder.add_edge("web_search", "post_process")
        graph_builder.set_finish_point("post_process")
        return graph_builder.compile()

    def web_search(self, state: AgentState) -> dict:
        grounding_llm = GroundingLLM()
        response = grounding_llm(state["search_query"])

        if grounding_llm.include_citations:
            result = grounding_llm.map_text_with_citations(response.to_dict())
        else:
            result = response.text

        display_message_dict = {
            "role": "assistant",
            "title": "Web Searcherの検索結果",
            "icon": "🔍",
            "content": result,
        }

        return {
            "messages": AIMessage(result),
            "display_message_dict": display_message_dict,
        }

    def post_process(self, state: AgentState) -> dict:
        message = AIMessage("Web検索が完了しました。")
        return {"messages": message, "display_message_dict": None}
