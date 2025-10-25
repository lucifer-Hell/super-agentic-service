from typing import Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class ChatState(BaseModel):

    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        title="messages",
        description="The messages exchanged in the conversation",
        default=[]
    )

    userName: str = Field(
        title="name",
        description="The name of the user",
    )

    language: str = Field(
        title="language",
        description="The language in which user would like to communicate it can be either english or hindi",
        default="English"
    )

    voice_response: str = Field(
        title="voice response",
        description="The voice response of the ai",
    )

    html_response: str = Field(
        title="visual response",
        description="The html response of the ai",
    )


