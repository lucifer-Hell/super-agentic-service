from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

import llm_providers.openai_llm as openai_llm
from workflows.test_workflow.tools.tools import register_user


class AgentResponse(BaseModel):
    name: str | None = Field(
        title="name",
        description="The name of the user",
        default=None,
    )
    isNamePresent: bool = Field(
        title="isNamePresent",
        description="Whether the name of the user is present",
        default=False,
    )


agent = create_react_agent(
    model=openai_llm.llm,
    tools=[],
    prompt="You are an agent whose only task is to generate a structured response containing 'name' and 'isNamePresent'. "
           "Based on the below messages, determine if the user's name is present. "
           "If the name is not present, return 'isNamePresent': false and 'name': None. "
           "If the name can be found from the messages, return 'isNamePresent': true and 'name' as the concluded name. "
           "Do not perform any other actions. ",
    name="user_info_agent",
    response_format=AgentResponse
)