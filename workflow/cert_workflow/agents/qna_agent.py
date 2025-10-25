from typing import Literal, List

from langchain_core.messages import AIMessage, HumanMessage
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
    )

@tool
def retrieve_context(query:str) -> str:
    """
    Always call this tool to fetch the context related to user query
    Always make sure to pass query in input
    Response you will be getting as List[dict]
    """
    service = RetrieverService()
    print(f"called retrieve context with query: {query}")
    results = service.retrieve_data(query)
    if not results:
        return "No information found."
    formatted = "\n".join([r["content"] for r in results])
    # return f"Here are some facts I found:\n{formatted}"
    return f"Photosynthesis is the process of creating a photo base(Source: ScienceKids)"


prompt = """
You are a helpful QnA Agent for children. Your job is to answer using only what your tools return.

VERY IMPORTANT:
- Read carefully the information that tools return (after "Observation:").
- Use those facts directly in your answer.
- Do not answer from your own knowledge if the tool returns data.
- If tool returns empty or 'No information found', then say:
    response: "At the moment I don't have any answer for this."
    has_answer: False
...
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



# def qna_agent_node(state: ChatState) -> dict:
#     """"""
#     # Get the response from the QnA agent
#     # TODO THIS ISN'T WORKING
#     result = qna_agent.invoke({'messages': state.messages})
#     result: QnAAgentResponse = result["structured_response"]
#     if result.has_answer:
#         return {
#             "messages": AIMessage(
#                 content=result.response
#             )
#         }
#     else:
#         return {
#         "messages": AIMessage(
#         content="As of now i don't have answer , is there any other question i can help"
#          )
#     }



def qna_agent_node(state: ChatState) -> dict:
    """
    QnA Agent node that:
      1. Retrieves relevant context from the retriever tool.
      2. Builds a grounded prompt using *all prior messages* for continuity.
      3. Forces the LLM to answer ONLY using that context.
    """

    # --- Step 1: extract the latest user question ---
    messages = state.messages
    user_question = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            user_question = msg.content
            break

    if not user_question:
        raise ValueError("No user message found in conversation state.")

    # --- Step 2: fetch relevant context ---
    context = retrieve_context.invoke({"query": user_question})

    # --- Step 3: build full conversational grounding prompt ---
    conversation_text = "\n".join([
        f"Human: {m.content}" if isinstance(m, HumanMessage)
        else f"Assistant: {m.content}"
        for m in messages
    ])

    grounded_prompt = f"""
You are a friendly children's Q&A assistant.
You must answer using ONLY the information inside the 'Context' section.
If the context does not contain an answer, say:
    response: "At the moment I don't have any answer for this."
    has_answer: False

Be simple, kind, and curious.

Conversation so far:
{conversation_text}

Context:
{context}

Now answer the last user question again, grounding your answer strictly in the Context.
    """

    # --- Step 4: structured call ---
    llm = openai_llm.llm.with_structured_output(QnAAgentResponse)
    result: QnAAgentResponse = llm.invoke(grounded_prompt)

    # --- Step 5: respond back into chat graph ---
    return {
        "messages": AIMessage(content=result.response)
    }