# AGENTS ONLY TASK IS TO RETURN OUTPUT DECIDING NEXT SET OF AGENT TO BE CALLED
from langchain_openai import OpenAI, ChatOpenAI
from langgraph.prebuilt import create_react_agent


from langgraph_supervisor import create_supervisor
from langgraph.store.memory import InMemoryStore
from langchain.chat_models import init_chat_model

import llm_providers.openai_llm as openai_llm
from agents.greet_agent import agent as greet_agent
from agents.joke_agent import agent as joke_agent

supervisor = create_supervisor(
    model=openai_llm.llm,
    agents=[ greet_agent, joke_agent],
    prompt=(
        "You are a supervisor managing four agents:\n"
        "- a greet agent. Assign greeting tasks to this agent. If the user's name is not provided, ask for it.\n"
        "- a joke agent. Assign joke-telling tasks to this agent.\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()