import os
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode


def get_tools(tavily_api_key=None):
    key = (tavily_api_key or os.environ.get("TAVILY_API_KEY", "")).strip()
    if not key:
        raise ValueError("Please enter your Tavily API key (or set TAVILY_API_KEY).")
    return [TavilySearch(max_results=2, tavily_api_key=key)]


def create_tool_node(tools):
    return ToolNode(tools=tools)
