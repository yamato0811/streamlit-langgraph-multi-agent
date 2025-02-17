import streamlit as st


def display_message(message: dict) -> None:
    """
    messageをstreamlit上に表示する関数
    """
    with st.chat_message(message["role"]):
        with st.expander(
            message["title"],
            expanded=True,
            icon=message["icon"],
        ):
            st.write(message["content"], unsafe_allow_html=True)


def display_messages(messages: list[dict]) -> None:
    """
    streamlit上で過去のメッセージをすべて表示する関数
    """
    for message in messages:
        display_message(message)
