from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

import llm_providers.openai_llm as openai_llm
from workflows.ivr_workflow.tools.tools import register_user


class AgentResponse(BaseModel):
    response: str = Field(
        title="response",
        description="The response from the agent",
        default=None,
    )


agent = create_react_agent(
    model=openai_llm.llm,
    tools=[register_user],
    prompt="You are an agent that only asks the user for their name if user hasn't provided till now , once user provided the name you update the state using the register_user ,then you greet the user using their name"
           "you cannot respond to anything else only task is to reply to user for requesting there usernmae if not yet provided"
           "Below is the conversation history"
           "{messages}",
    name="user_info_agent",
    response_format=AgentResponse
)