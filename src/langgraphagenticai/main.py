import streamlit as st
from src.langgraphagenticai.ui.streamlit.loadui import LoadStreamLitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graphs.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlit.display_result import DisplayResultStreamlit


def load_langgraph_agenticai_app():
    """Load the Streamlit UI, build the LLM + graph, and run one chat turn."""
    ui = LoadStreamLitUI()
    user_input = ui.load_streamlit_ui()

    user_message = st.chat_input("Enter your message: ")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    display = DisplayResultStreamlit()
    display.render_history()

    if not user_message:
        return

    usecase = user_input.get("selected_usecase")
    if not usecase:
        st.error("Error: No use case selected")
        return

    try:
        model = GroqLLM(user_controls_input=user_input).get_llm_model()
    except Exception as e:
        st.error(f"LLM setup failed: {e}")
        return

    try:
        graph = GraphBuilder(model).setup_graph(usecase)
    except Exception as e:
        st.error(f"Graph setup failed: {e}")
        return

    try:
        display.run_and_display(usecase, graph, user_message)
    except Exception as e:
        st.error(f"Chat run failed: {e}")
