import streamlit as st
from langchain_core.messages import HumanMessage

from src.langgraphagenticai.ui.streamlit.loadui import LoadStreamLitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graphs.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlit.display_result import DisplayResultStreamlit


def _build_graph(user_input, usecase):
    """Returns a compiled graph, or None after showing the error."""
    try:
        model = GroqLLM(user_controls_input=user_input).get_llm_model()
    except Exception as e:
        st.error(f"LLM setup failed: {e}")
        return None
    try:
        return GraphBuilder(
            model, tavily_api_key=user_input.get("TAVILY_API_KEY")
        ).setup_graph(usecase)
    except Exception as e:
        st.error(f"Graph setup failed: {e}")
        return None


def _run_ai_news(user_input, display):
    if user_input.get("fetch_news_clicked"):
        graph = _build_graph(user_input, "AI News")
        if graph is not None:
            try:
                with st.spinner("Fetching and summarizing news..."):
                    st.session_state.news_result = graph.invoke(
                        {"messages": [HumanMessage(content=user_input["time_frame"])]}
                    )
            except Exception as e:
                st.error(f"AI News run failed: {e}")

    # keep showing the last result across reruns (e.g. after a download click)
    if st.session_state.get("news_result"):
        display.render_news(st.session_state.news_result)


def _run_chat(user_input, usecase, display):
    user_message = st.chat_input("Enter your message: ")
    display.render_history()
    if not user_message:
        return

    graph = _build_graph(user_input, usecase)
    if graph is None:
        return
    try:
        display.run_and_display(usecase, graph, user_message)
    except Exception as e:
        st.error(f"Chat run failed: {e}")


def load_langgraph_agenticai_app():
    """Load the Streamlit UI and run the selected use case."""
    ui = LoadStreamLitUI()
    user_input = ui.load_streamlit_ui()

    usecase = user_input.get("selected_usecase")
    if not usecase:
        st.error("Error: No use case selected")
        return

    display = DisplayResultStreamlit()
    if usecase == "AI News":
        _run_ai_news(user_input, display)
    else:
        _run_chat(user_input, usecase, display)
