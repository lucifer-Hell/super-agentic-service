from typing import TypedDict
from langgraph.graph import StateGraph, END, START
from agents.greet_agent import agent as greet_agent
from agents.joke_agent import agent as joke_agent

class State(TypedDict):
    name: str | None
    input: str | None
    output: str | None
    decision: str | None

# Node: greet
def greet_node(state: State):
    result = greet_agent.run({"name": state["name"]})
    state["output"] = result["greeting"]
    return state

# Node: joke
def joke_node(state: State):
    result = joke_agent.run({"name": state["name"]})
    state["output"] = result["joke"]
    return state

# Router node: decide next step
def router_node(state: State):
    if not state["name"]:
        return {"decision": "greet"}
    else:
        return {"decision": "joke"}

# Routing function
def route_decision(state: State):
    if state.get("decision") == "greet":
        return "greet_node"
    elif state.get("decision") == "joke":
        return "joke_node"

# Build workflow
graph = StateGraph(State)
graph.add_node("greet_node", greet_node)
graph.add_node("joke_node", joke_node)
graph.add_node("router_node", router_node)

graph.add_edge(START, "router_node")
graph.add_conditional_edges(
    "router_node",
    route_decision,
    {
        "greet_node": "greet_node",
        "joke_node": "joke_node",
    },
)
graph.add_edge("greet_node", END)
graph.add_edge("joke_node", END)

test_workflow = graph.compile()

# Usage example:
# state = {"name": None, "input": None, "output": None}
# result = test_workflow.invoke(state)
# print(result["output"])
