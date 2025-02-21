from typing import Annotated

from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId


@tool
def handoff_to_web_searcher(
    search_query: Annotated[
        str,
        "ユーザーが検索したい内容が記載されたテキスト",
    ],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> dict:
    """
    ユーザーが検索したい内容を受け取り、web_searcherに引き継ぎます。
    ユーザーが検索を必要としている場合、このツールを呼び出します。

    web_searcherの役割は以下の通り
    - ユーザーの要望に基づいてWeb検索を行い、その結果を整理して返します。
    """
    print("## Called Web Searcher")

    tool_msg = {
        "role": "tool",
        "content": "Successfully transferred to Web Searcher.",
        "tool_call_id": tool_call_id,
    }

    return {
        "goto": "web_searcher_subgraph",
        "update": {"messages": [tool_msg], "search_query": search_query},
    }


@tool
def handoff_to_copy_generator(
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> dict:
    """
    コピー生成を行うために、copy_generatorに引き継ぎます。
    ユーザーがコピー生成を要望している場合、このツールを呼び出します。

    copy_generatorの役割は以下の通り
    - テーマに基づいてコピー文を生成します
    """
    print("## Called Copy Generator")

    tool_msg = {
        "role": "tool",
        "content": "Successfully transferred to Copy Generator.",
        "tool_call_id": tool_call_id,
    }

    return {
        "goto": "copy_generator_subgraph",
        "update": {"messages": [tool_msg]},
    }
