from typing import Literal

from langchain.agents import create_structured_chat_agent
from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from llm_providers import openai_llm
from workflows.voice_workflow.state.voice_state import VoiceState

# Response Model for QnA Agent
class QnAAgentResponse(BaseModel):
    # Response fields for QnA agent
    response: str = Field(
        description="this field must have the same response which agent gives"
    )

prompt = """
You are a QnA Agent. Your task is to respond to the user's query in the best possible way.

Guidelines:
- Provide a clear and concise response to the user's query.
- Avoid adding follow-up questions, conversational elements, or emojis.
- Ensure the response is helpful and directly addresses the user's question.

Examples:
1. User: "What is the refund policy?"
   Response: "Our refund policy allows returns within 30 days of purchase with a valid receipt."

2. User: "How can I reset my password?"
   Response: "To reset your password, click on 'Forgot Password' on the login page and follow the instructions."

Do not perform any other actions.
"""

qna_agent = create_react_agent(
    model=openai_llm.llm,
    tools=[],
    prompt=prompt,
    name="qna_agent",
    response_format=QnAAgentResponse
)

def qna_agent_node(state: VoiceState) -> dict:
    # Get the response from the QnA agent
    result = qna_agent.invoke({"messages": state.messages})
    result: QnAAgentResponse = result["structured_response"]

    return {
        "messages": AIMessage(
            content=result.response + " If you are not satisfied with my response please say create ticket and i will create a support ticket for you."
        )
    }
