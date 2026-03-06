from dataclasses import dataclass, field
from typing import Annotated, Dict

from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages


@dataclass
class EmailSchema:
    email: str
    email_category: str = ""
    email_response: str = ""
    masked_email_response: str = ""
    email_tone: str = ""
    masked_email: str = ""
    masked_email_entites: Dict = field(default_factory=dict)
    messages: Annotated[list[BaseMessage], add_messages] = field(default_factory=list)
