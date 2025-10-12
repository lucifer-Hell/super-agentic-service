from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from workflow.voice_workflow.agents.end_call_agent import end_call_agent_node
from workflow.voice_workflow.agents.qna_agent import qna_agent_node
from workflow.voice_workflow.agents.router_agent import router_agent_node
from workflow.voice_workflow.agents.short_id_agent import  short_id_agent_node
from workflow.voice_workflow.agents.ticket_agent import ticket_agent_node
from workflow.voice_workflow.state.voice_state import VoiceState

voice_workflow = StateGraph(VoiceState)

# Add nodes
voice_workflow.add_node("short_id_agent", short_id_agent_node)
voice_workflow.add_node("qna_agent", qna_agent_node)
voice_workflow.add_node("ticket_agent", ticket_agent_node)
voice_workflow.add_node("router_agent", router_agent_node)
voice_workflow.add_node("end_call_agent", end_call_agent_node)


# Define edges
#  ROUTER -> NEXT AGNET
voice_workflow.add_edge(START, "router_agent")
voice_workflow.add_conditional_edges(
    "router_agent",
    lambda agent_output: agent_output.call_agent,
    {
        "short_id_agent":"short_id_agent",
        "qna_agent": "qna_agent",
        "ticket_agent": "ticket_agent",
        "end_call_agent":"end_call_agent"
    }
)

# ADD END EDGES
voice_workflow.add_edge("short_id_agent", END)
voice_workflow.add_edge("qna_agent", END)
voice_workflow.add_edge("ticket_agent", END)
voice_workflow.add_edge("end_call_agent", END)

# define storage
memory = InMemorySaver()

# compile workflow
voice_workflow = voice_workflow.compile(checkpointer=memory)


