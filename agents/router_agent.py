import llm_providers.openai_llm as openai_llm
from agents.greet_agent import agent as greet_agent
from agents.joke_agent import agent as joke_agent


from langgraph_supervisor import create_supervisor

supervisor = create_supervisor(
    model=openai_llm.llm,
    agents=[greet_agent, joke_agent],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- a joke agent. Assign joke tasks to this agent\n"
        "- a greet agent. Assign greeting related tasks to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
).compile()