import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

SUPPORTED_USECASES = ("Basic Chatbot", "Chatbot with Web")


def _show(message):
    """Render one message. Returns nothing; skips empty AI messages (pure tool calls)."""
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, ToolMessage):
        with st.chat_message("assistant"):
            with st.expander(f"Tool call: {message.name or 'tool'}"):
                st.write(message.content)
    elif isinstance(message, AIMessage) and message.content:
        with st.chat_message("assistant"):
            st.write(message.content)


class DisplayResultStreamlit:
    """Streamlit reruns the script on every input, so history lives in session_state."""

    def render_history(self):
        for msg in st.session_state.setdefault("chat_history", []):
            _show(msg)

    def run_and_display(self, usecase, graph, user_message):
        if usecase not in SUPPORTED_USECASES:
            st.warning(f"Unsupported use case: {usecase}")
            return

        history = st.session_state.setdefault("chat_history", [])

        human = HumanMessage(content=user_message)
        history.append(human)
        _show(human)

        result = graph.invoke({"messages": history})

        # Everything after what we already had = new AI / tool messages.
        for message in result["messages"][len(history):]:
            history.append(message)
            _show(message)
