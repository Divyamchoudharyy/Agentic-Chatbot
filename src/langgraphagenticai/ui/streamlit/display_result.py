import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage


class DisplayResultStreamlit:
    """Streamlit reruns the script on every input, so history lives in session_state."""

    def render_history(self):
        for msg in st.session_state.chat_history:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            with st.chat_message(role):
                st.write(msg.content)

    def run_and_display(self, usecase, graph, user_message):
        if usecase != "Basic Chatbot":
            st.warning(f"Unsupported use case: {usecase}")
            return

        with st.chat_message("user"):
            st.write(user_message)

        history = st.session_state.chat_history
        history.append(HumanMessage(content=user_message))

        result = graph.invoke({"messages": history})
        reply = result["messages"][-1]

        if isinstance(reply, AIMessage) and reply.content:
            history.append(reply)
            with st.chat_message("assistant"):
                st.write(reply.content)
