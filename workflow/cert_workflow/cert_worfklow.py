from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from workflow.cert_workflow.agents.qna_agent import qna_agent_node
from workflow.cert_workflow.states.cert_state import ChatState

cert_workflow = StateGraph(ChatState)

# Add nodes
cert_workflow.add_node("qna_agent",qna_agent_node)

# Define edges
cert_workflow.add_edge(START, "qna_agent")
cert_workflow.add_edge( "qna_agent",END)
# ADD MEMORY
memory = InMemorySaver()

# Compile workflow
cert_workflow = cert_workflow.compile(checkpointer=memory)

