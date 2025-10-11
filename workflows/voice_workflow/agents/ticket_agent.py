from typing import Literal

from langchain.agents import create_structured_chat_agent
from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from llm_providers import openai_llm
from workflows.voice_workflow.state.voice_state import VoiceState

# Response Model for Ticket Content Extract Agent
class TicketContentExtractResponse(BaseModel):
    # Response fields for ticket content extraction
    summarized_content: str = Field(
        description="A summarized version of the entire conversation for ticket creation"
    )

prompt = """
You are a Ticket Content Extract Agent. Your task is to extract and summarize the entire conversation into a concise format suitable for creating a ticket.

Guidelines:
- Summarize the entire conversation, including both user and system messages, into a clear and concise format.
- Ensure the summary captures the key details necessary for ticket creation.

Examples:
1. Conversation:
   User: "I am facing an issue with my internet connection. It keeps disconnecting every few minutes."
   System: "Have you tried restarting your router?"
   User: "Yes, I have, but the issue persists."
   Response: summarized_content = 'User reports frequent internet disconnections despite restarting the router.'

2. Conversation:
   User: "The app crashes whenever I try to upload a file."
   System: "Can you confirm if this happens with all file types?"
   User: "Yes, it happens with all file types."
   Response: summarized_content = 'App crashes during file uploads regardless of file type.'

Do not perform any other actions.
"""

ticket_content_extract_agent = create_react_agent(
    model=openai_llm.llm,
    tools=[],
    prompt=prompt,
    name="ticket_content_extract_agent",
    response_format=TicketContentExtractResponse
)

def ticket_agent_node(state: VoiceState) -> dict:
    # Extract ticket content using the agent
    result = ticket_content_extract_agent.invoke({"messages": state.messages})
    result: TicketContentExtractResponse = result["structured_response"]

    if result.summarized_content:
        import random
        ticket_number = " ".join(str(random.randint(10000, 99999)))
        return {
            "messages": AIMessage(
                content=f"Your ticket has been created successfully. Your ticket number is {ticket_number}. How can I assist you further?"
            )
        }
    else:
        return {
            "messages": AIMessage(
                content="I could not extract the details for your ticket. Can you please provide the information so I can create a ticket?"
            )
        }
