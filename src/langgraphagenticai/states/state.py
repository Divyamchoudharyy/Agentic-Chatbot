from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class State(TypedDict, total=False):
    """Graph state. LangGraph silently DROPS any key not declared here."""
    messages: Annotated[List, add_messages]
    # AI News use case
    frequency: str      # "daily" | "weekly" | "monthly"
    news_data: list     # raw Tavily results
    summary: str        # markdown digest from the LLM
    filename: str       # saved .md path
