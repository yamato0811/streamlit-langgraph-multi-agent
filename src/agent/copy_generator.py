from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from agent.state import AgentState
from models.llm import LLM


class CopyGenerator:
    def __init__(self, llm: LLM) -> None:
        self.llm = llm
        self.graph = self.build_graph()

    def build_graph(self) -> CompiledStateGraph:
        graph_builder = StateGraph(AgentState)
        graph_builder.add_node(self.copy_generate)
        graph_builder.add_node(self.copy_improvement)
        graph_builder.add_node(self.post_process)

        graph_builder.set_entry_point("copy_generate")
        graph_builder.add_edge("copy_generate", "copy_improvement")
        graph_builder.add_edge("copy_improvement", "post_process")
        graph_builder.set_finish_point("post_process")
        return graph_builder.compile()

    def copy_generate(self, state: AgentState) -> dict:
        response = self.llm(
            [
                (
                    "system",
                    "あなたはプロのコピーライターです。",
                )
            ]
            + state["messages"]
            + [
                {
                    "role": "human",
                    "content": "会話の内容をもとにキャッチコピーを1つ生成してください。結果のみ出力してください。",
                }
            ]
        )

        return {
            "messages": response,
            "copy": response.content,
        }

    def copy_improvement(self, state: AgentState) -> dict:
        response = self.llm(
            [
                (
                    "system",
                    "あなたはプロのコピーライターです。",
                )
            ]
            + state["messages"]
            + [
                {
                    "role": "human",
                    "content": "1つのキャッチコピーを改善してください。結果のみ出力してください。",
                }
            ]
        )

        return {
            "messages": response,
            "copy": response.content,
        }

    def post_process(self, state: AgentState) -> dict:
        message = AIMessage("コピー生成が完了しました。")
        return {"messages": message}
