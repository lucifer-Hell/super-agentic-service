# VOICE FLOW STATE
from typing import Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class VoiceState(BaseModel):
    shortId: str | None = Field(
        title="shortId",
        description="The short identification number of the user",
        default=None,
    )
    isNamePresent: bool = Field(
        title="isNamePresent",
        description="Whether the name of the user is present",
        default=False,
    )
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        title="messages",
        description="The messages exchanged in the conversation",
        default=[],
    )

    call_agent:str = Field(
        title="call_agent",
        description="The next agent to be called",
        default=None
    )