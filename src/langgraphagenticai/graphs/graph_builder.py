from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition

from src.langgraphagenticai.states.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.nodes.chatbot_tools_node import ChatbotToolNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node


class GraphBuilder:
    def __init__(self, model, tavily_api_key=None):
        self.llm = model
        self.tavily_api_key = tavily_api_key
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """START -> chatbot -> END"""
        basic_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot", basic_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_tools_build_graph(self):
        """START -> chatbot -> (tools -> chatbot)* -> END"""
        tools = get_tools(self.tavily_api_key)
        tool_node = create_tool_node(tools)
        chatbot_node = ChatbotToolNode(self.llm).create_chatbot(tools)

        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        self.graph_builder.add_edge(START, "chatbot")
        # tools_condition -> "tools" if the LLM asked for a tool, else END
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

    def setup_graph(self, usecase: str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot with Web":
            self.chatbot_tools_build_graph()
        else:
            raise ValueError(f"Unsupported use case: {usecase}")

        return self.graph_builder.compile()
