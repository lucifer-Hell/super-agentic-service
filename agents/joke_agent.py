from langgraph.prebuilt import create_react_agent

import llm_providers.openai_llm as openai_llm

agent = create_react_agent(
    model=openai_llm.llm,
    tools=[],
    prompt="You are a friendly agent that generates a random joke on software engineers",
    name="joke_agent",
)