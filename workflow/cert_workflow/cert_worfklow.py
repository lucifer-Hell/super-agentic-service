
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

import llm_providers.openai_llm
from workflow.cert_workflow.states.cert_state import ChatState

class QnaAgentResponseDto(BaseModel):
    can_answer: bool = Field(
        description="Whether the agent can answer the question",
    )
    answer: str = Field(
        description="The answer to the question",
    )

@tool
def retriever(query:str)->str:
    """
    This tool retrieves relevant documents based on the query.
    """
    return "The process of photosynthesis is to take a photo and apply filters on it"


def qna_agent_node(state:ChatState)->dict:
    qna_agent = create_agent(
        model = llm_providers.openai_llm.llm,
        response_format=QnaAgentResponseDto,
        tools=[retriever],
        system_prompt="""
        You are Alex an AI assistant that helps users with their queries. You have access to a tool called retriever which you can use to get relevant documents based on the user's question. 
        Only answer the question based on the retrieved documents. If you cannot find the answer in the documents, respond with "I don't have any information about this at the moment".
        """,
        debug=True
    )

    response = qna_agent.invoke({"messages":state.messages})
    print(response)
    return{
        "messages":AIMessage(
            content="Hi i am alex how can i help you?"
        )
    }



cert_workflow = StateGraph(ChatState)
# Steps to build
# 1. Take the user input and the message history and generate a summarized question --> create agent which is going to generate a summarized query
# 2. Can the question be answered with current message history if no then call retriever agent else directly call the answer agent
# 2. Use the summarized question to retrieve relevant documents --> retriever agent whom query is passed answer the user question
# 3. Use the relevant documents and the message history to generate a response
# 4. Frame the response into answer

# Add nodes
cert_workflow.add_node("qna_agent",qna_agent_node)

# Define edges
cert_workflow.add_edge(START, "qna_agent")
cert_workflow.add_edge( "qna_agent",END)
# ADD MEMORY
memory = InMemorySaver()

# Compile workflow
cert_workflow = cert_workflow.compile(checkpointer=memory)

