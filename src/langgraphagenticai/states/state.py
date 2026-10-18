from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class State(TypedDict):
    """Graph state: running list of chat messages (appended via add_messages)."""
    messages: Annotated[List, add_messages]
