from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from commons.agents import joke_agent
from workflows.ivr_workflow.agents.user_info_agent import agent as user_info_agent, AgentResponse
from workflows.ivr_workflow.agents.ivr_router import router_agent
from workflows.ivr_workflow.state.ivr_state import IVRState

# Intitalize workflow with state
ivr_workflow= StateGraph(IVRState)

# Add nodes
def user_info_agent_node(state:IVRState)-> dict :
    result = user_info_agent.invoke({"messages":state.messages})
    result:AgentResponse= result["structured_response"]
    name:str = result.name
    isNamePresent = result.isNamePresent
    message = "Hello " + name + " what joke would you like to hear today " if isNamePresent else "Can you please tell your name to proceed ?"
    message= AIMessage(content=message)
    return  {
        "messages":message,
        "name":name,
        "isNamePresent":isNamePresent
    }



ivr_workflow.add_node("user_info_agent", user_info_agent_node)
ivr_workflow.add_node("joke_agent", joke_agent.agent)
ivr_workflow.add_node("router_agent",router_agent)

# Define edges
ivr_workflow.add_edge(START, "router_agent")
ivr_workflow.add_conditional_edges(
    "router_agent",
            lambda agent_output : agent_output.call_agent,
    {
        "user_info_agent": "user_info_agent",
        "joke_agent": "joke_agent",
    }
)
ivr_workflow.add_edge("user_info_agent", END)
ivr_workflow.add_edge("joke_agent", END)

# Compile
memory = InMemorySaver()

ivr_workflow = ivr_workflow.compile(checkpointer=memory)
