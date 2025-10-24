from typing import Literal, List

from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from llm_providers import openai_llm
from service.retriever_service import RetrieverService
from workflow.cert_workflow.states.cert_state import ChatState
from workflow.voice_workflow.state.voice_state import VoiceState
from langchain.tools import tool

# Response Model for QnA Agent
class QnAAgentResponse(BaseModel):
    # Response fields for QnA agent
    response: str = Field(
        description="this field contains a summarized version of agent response"
    )
    has_answer:bool = Field(
        description="this field indicates if the agent was able to come an answer",
        default=False,
    )

@tool
def retrieve_context(query:str) -> List[dict]:
    """
    Always call this tool to fetch the context related to user query
    Always make sure to pass query in input
    Response you will be getting as List[dict]
    """
    service = RetrieverService()
    print(f"called retrieve context with query: {query}")
    return service.retrieve_data(query)

prompt = """
You are a helpful QnA Agent for children. Your job is to answer their questions using only the information from the tools you have. Never make up answers—always use what you find with your tools.

Guidelines:
- Give answers that are easy for children to understand.
- Use simple words and friendly sentences.
- Encourage curiosity by adding a fun fact or a follow-up question.
- Never guess or invent information. Only use what your tools provide.
- If you don't have an answer, give 
    response: "At the moment I don't have any answer for this."
    has_answer: False

Examples:
1. Child: "Why do birds sing?"
   Response: "Birds sing to talk to each other and sometimes to find friends. Did you know some birds can copy sounds they hear? What sound would you like a bird to copy?"
    has_answer: True

2. Child: "How do plants grow?"
   Response: "Plants grow by using sunlight, water, and air. Their leaves catch sunlight to make food. Have you ever tried growing a plant from a seed?"
    has_answer: True

Do not perform any other actions.
"""

qna_agent = create_react_agent(
    model=openai_llm.llm,
    tools=[
        retrieve_context
    ],
    prompt=prompt,
    name="qna_agent",
    response_format=QnAAgentResponse,
    debug=True,
)

def qna_agent_node(state: ChatState) -> dict:
    """"""
    # Get the response from the QnA agent
    # TODO THIS ISN'T WORKING
    result = qna_agent.invoke({"messages": state.messages})
    result: QnAAgentResponse = result["structured_response"]
    if result.has_answer:
        return {
            "messages": AIMessage(
                content=result.response
            )
        }
    else:
        return {
        "messages": AIMessage(
        content="As of now i don't have answer , is there any other question i can help"
         )
    }