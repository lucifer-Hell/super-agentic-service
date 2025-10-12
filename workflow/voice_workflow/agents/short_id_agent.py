from typing import Literal

from langchain.agents import create_structured_chat_agent
from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from llm_providers import openai_llm
from workflow.voice_workflow.state.voice_state import VoiceState


# Response Model for Short ID Agent
class ShortIdAgentResponse(BaseModel):
    # Response fields for Short ID extraction
    extracted_short_id: str = Field(
        description="The short ID extracted from the user's input"
    )
    is_extraction_successful: bool = Field(
        description="Indicates whether the extraction of the short ID was successful",
        default=False
    )

prompt = """
You are a Short ID Agent. Your task is to extract the short ID mentioned by the user from the provided input.

Guidelines:
- If a valid short ID is mentioned, extract it and set 'is_extraction_successful' to true.
- If no valid short ID is found, set 'extracted_short_id' to an empty string and 'is_extraction_successful' to false.

Examples:
1. User: "My short ID is k0230."
   Response: extracted_short_id = 'k02030', is_extraction_successful = true

2. User: "I don’t have a short ID."
   Response: extracted_short_id = '', is_extraction_successful = false

Do not perform any other actions.
"""

short_id_agent = create_react_agent(
    model=openai_llm.llm,
    tools=[],
    prompt=prompt,
    name="short_id_agent",
    response_format=ShortIdAgentResponse
)


def short_id_agent_node(state: VoiceState)-> dict:
    # get extracted short id from agent
    result = short_id_agent.invoke({"messages": state.messages})
    result: ShortIdAgentResponse = result["structured_response"]
    if result.is_extraction_successful:
        return{
            "shortId": result.extracted_short_id,
            "isShortIdValidated": True,
            "messages": AIMessage(
                content="Short id validated successfully. How can I assist you further?"
            )
        }
    else:
        return{
            "messages": AIMessage(
                content="Can you please provide your short id to proceed with "
            )
        }

