from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from workflow.cert_workflow.states.cert_state import ChatState

def qna_agent_node(state:ChatState)->dict:
    return{
        "messages":AIMessage(
            content="Hi i am alex how can i help you?"
        )
    }

cert_workflow = StateGraph(ChatState)
# Steps to build
# 1. Take the user input and the message history and generate a summarized question

# Add nodes
cert_workflow.add_node("qna_agent",qna_agent_node)

# Define edges
cert_workflow.add_edge(START, "qna_agent")
cert_workflow.add_edge( "qna_agent",END)
# ADD MEMORY
memory = InMemorySaver()

# Compile workflow
cert_workflow = cert_workflow.compile(checkpointer=memory)

