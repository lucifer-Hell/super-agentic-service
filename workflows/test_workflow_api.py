from fastapi import FastAPI
from pydantic import BaseModel
from workflows.test_workflow import test_workflow, State

app = FastAPI()

# Simple in-memory store for session states
session_memory = {}

class MessageModel(BaseModel):
    session_id: str
    message: str

@app.post("/test_workflow")
async def run_test_workflow(msg: MessageModel):
    # Retrieve previous state from memory or initialize
    state = session_memory.get(msg.session_id, State(name=None, input=None, output=None, decision=None))
    # Update state with new input
    state["input"] = msg.message
    try:
        result = test_workflow(state)
        # Update memory with new state (if workflow updated it, e.g., set name)
        session_memory[msg.session_id] = result
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
