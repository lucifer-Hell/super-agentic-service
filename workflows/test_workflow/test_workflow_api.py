from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from workflows.test_workflow.ivr_workflow import ivr_workflow

app = FastAPI()

class MessageModel(BaseModel):
    session_id: str
    message: str

@app.post("/test_workflow")
async def run_test_workflow(msg: MessageModel):

    try:
        # result = test_workflow(msg.message)
        config = {"configurable": {"thread_id": msg.session_id}}
        result =ivr_workflow.invoke({
            "messages": [HumanMessage(content=msg.message)]
        }, config=config
        )
        # Update memory with new state (if workflow updated it, e.g., set name)
        return {"response": result["messages"][-1].content}
    except Exception as e:
        return {"error": str(e)}
