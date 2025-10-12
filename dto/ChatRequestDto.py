from typing import List, Optional, Dict
import uuid
from pydantic import BaseModel, dataclasses
from dto.RequestAttributesDto import RequestAttributes


class MessageQuery(BaseModel):
    query: str
    type: Optional[str] = None
    stopConversation: Optional[bool] = None


class ChatTalkRequestDto(BaseModel):
    channelId: Optional[str] = None
    userId: Optional[uuid.UUID] = None
    verticalId: Optional[str] = None
    conversationId: str
    message: MessageQuery  # Replace with actual MessageQuery structure
    requestAttributes: RequestAttributes
