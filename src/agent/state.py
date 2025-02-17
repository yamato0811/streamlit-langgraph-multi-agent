from langgraph.graph.message import add_messages
from typing_extensions import Annotated, Literal, TypedDict


class DisplayMessageDict(TypedDict):
    role: Literal["user", "assistant"]
    title: str
    icon: str
    content: str


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

    copy: str
    search_query: str

    is_finished: bool
    display_message_dict: DisplayMessageDict
