from typing import Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class ChatState(BaseModel):

    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        title="messages",
        description="The messages exchanged in the conversation",
        default=[],
    )
