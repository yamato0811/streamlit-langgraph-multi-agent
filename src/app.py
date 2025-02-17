import streamlit as st
from dotenv import load_dotenv

from agent.copy_generator import CopyGenerator
from agent.supervisor import Supervisor
from agent.web_searcher import WebSearcher
from models.grounding_llm import GroundingLLM
from models.llm import LLM

load_dotenv()

MODEL = "gemini"
THREAD_ID = "1"
TEMPERATURE = 1.0


def main() -> None:
    # ================
    # Page Config
    # ================
    st.set_page_config(
        page_title="Streamlit×LangGraph MultiAgent | コピー生成アプリケーション",
        page_icon="🤖",
    )
    st.title("Streamlit×LangGraph MultiAgent | コピー生成アプリケーション")

    # ================
    # Init Actor
    # ================
    llm = LLM(MODEL, TEMPERATURE)
    grounding_llm = GroundingLLM()

    copy_generator = CopyGenerator(llm)
    web_searcher = WebSearcher(grounding_llm)
    supervisor = Supervisor(llm, copy_generator, web_searcher)

    # ================
    # User Input
    # ================
    user_input = st.chat_input("メッセージを入力してください:")
    if not user_input:
        st.stop()

    # ================
    # Core Algorithm
    # ================
    supervisor.write_mermaid_graph(supervisor.graph)

    inputs = {"messages": user_input}
    config = {"configurable": {"thread_id": THREAD_ID}}

    for event in supervisor.graph.stream(
        inputs, config, stream_mode="values", subgraphs=True
    ):
        if display_message_dict := event[1].get("display_message_dict"):
            with st.chat_message(display_message_dict["role"]):
                with st.expander(
                    display_message_dict["title"],
                    expanded=True,
                    icon=display_message_dict["icon"],
                ):
                    st.write(display_message_dict["content"], unsafe_allow_html=True)


if __name__ == "__main__":
    main()
