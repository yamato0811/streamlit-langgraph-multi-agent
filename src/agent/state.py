from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

    copy: str
    search_query: str
    is_finished: bool
