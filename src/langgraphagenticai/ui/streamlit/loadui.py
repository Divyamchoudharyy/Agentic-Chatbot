
import streamlit as st
from src.langgraphagenticai.ui.uiconfigfile import Config


class LoadStreamLitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        page_title = self.config.get_page_title()

        st.set_page_config(
            page_title=page_title,
            layout="wide"
        )
        st.header(page_title)

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox(
                "Select LLM",
                llm_options
            )

            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()

                self.user_controls["selected_groq_model"] = st.selectbox(
                    "Select Model",
                    model_options
                )

                api_key = st.text_input(
                    "API Key",
                    type="password",
                    key="GROQ_API_KEY"
                )
                self.user_controls["GROQ_API_KEY"] = api_key

                if not api_key:
                    st.warning("Please enter your Groq API key to proceed.")

            self.user_controls["selected_usecase"] = st.selectbox(
                "Select Use Case",
                usecase_options
            )

            usecase = self.user_controls["selected_usecase"]

            if usecase in ("Chatbot with Web", "AI News"):
                tavily_key = st.text_input(
                    "Tavily API Key",
                    type="password",
                    key="TAVILY_API_KEY"
                )
                self.user_controls["TAVILY_API_KEY"] = tavily_key

                if not tavily_key:
                    st.warning("Please enter your Tavily API key to proceed.")

            if usecase == "AI News":
                self.user_controls["time_frame"] = st.selectbox(
                    "Select Time Frame",
                    ["Daily", "Weekly", "Monthly"],
                    index=0
                )
                # st.button is True only on the rerun right after the click
                self.user_controls["fetch_news_clicked"] = st.button(
                    "Fetch Latest AI News",
                    use_container_width=True
                )

        if self.user_controls["selected_usecase"] == "AI News":
            st.subheader("AI NEWS EXPLORER")

        return self.user_controls
