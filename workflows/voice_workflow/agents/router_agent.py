from typing import Literal

from langchain.agents import create_structured_chat_agent
from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from llm_providers import openai_llm
from workflows.voice_workflow.state.voice_state import VoiceState


# Response Model for Router Agent
class RouterAgentResponse(BaseModel):
    # Tell which agents should it route to
    next_agent: Literal[
        "qna_agent", "ticket_agent"
    ] = Field(
        description="The next agent to route to"
    )
    reason: str = Field(
        description="The reason the router agent is responsible"
    )


prompt = """
You are a router agent whose only task is to generate a structured response containing 'next_agent'
and 'reason'. Based on the below messages, determine which agent to route to.

The possible agents to route to are:
1. qna_agent: for general questions and answers
2. ticket_agent: for creating tickets

Guidelines:
- If the user is asking questions or seeking information, route to 'qna_agent'.
- If the user explicitly requests to create a ticket, expresses dissatisfaction, or indicates they do not understand the information provided, route to 'ticket_agent'.

Examples:
1. User: "Can you tell me about the refund policy?"
   Response: next_agent = 'qna_agent', reason = 'User is asking a general question.'

2. User: "I am not happy with the service. Please create a ticket."
   Response: next_agent = 'ticket_agent', reason = 'User is dissatisfied and explicitly requested to create a ticket.'

3. User: "I don’t understand the instructions you provided."
   Response: next_agent = 'ticket_agent', reason = 'User is not satisfied and needs further assistance.'

Do not perform any other actions.
"""

router_agent = create_react_agent(
    model=openai_llm.llm,
    tools=[],
    prompt=prompt,
    name="router_agent",
    response_format=RouterAgentResponse
)



# create node for router agent
def router_agent_node(state: VoiceState)->dict:
    if not state.isShortIdValidated:
        return {"call_agent": "short_id_agent"}

    result = router_agent.invoke({"messages": state.messages})
    #  cast the result to RouterAgentResponse
    result:RouterAgentResponse= result["structured_response"]
    # create ai message for the reason
    ai_message = generate_ai_message(result)

    return {
        "messages": ai_message,
        "call_agent": result.next_agent
    }


# UTIL FUNC
def generate_ai_message(result):
    ai_message = "Calling " + result.next_agent + " because " + result.reason
    ai_message = AIMessage(content=ai_message)
    return ai_message
