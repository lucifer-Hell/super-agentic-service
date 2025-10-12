from typing import List, Optional, Dict
import uuid
from pydantic import BaseModel, dataclasses
from dto.RequestAttributesDto import RequestAttributes


class MessageQuery(BaseModel):
    query: str
    type: Optional[str]
    stopConversation: Optional[bool]


class ChatResponseDto(BaseModel):
    longText: Optional[str]
    shortText: Optional[str]
