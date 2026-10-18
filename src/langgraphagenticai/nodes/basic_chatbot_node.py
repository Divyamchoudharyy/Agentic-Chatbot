from src.langgraphagenticai.states.state import State


class BasicChatbotNode:
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        return {"messages": [self.llm.invoke(state["messages"])]}
