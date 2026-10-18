import os
from langchain_groq import ChatGroq


class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        groq_api_key = (
            self.user_controls_input.get("GROQ_API_KEY", "").strip()
            or os.environ.get("GROQ_API_KEY", "").strip()
        )
        selected_model = self.user_controls_input.get("selected_groq_model")

        if not groq_api_key:
            raise ValueError("Please enter your Groq API key (or set GROQ_API_KEY).")
        if not selected_model:
            raise ValueError("No Groq model selected.")

        return ChatGroq(api_key=groq_api_key, model=selected_model)
