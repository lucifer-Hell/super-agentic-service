from typing import TypedDict
from agents.router_agent import supervisor

class State(TypedDict):
    name: str | None
    input: str | None
    output: str | None
    decision: str | None

# Main workflow function using LLM-powered supervisor

def test_workflow(state: State):
    # Pass the state to the supervisor agent, which will use the LLM to route and call agents
    result = supervisor.invoke(state)
    return result
