from typing import TypedDict
from agents.router_agent import supervisor

# Main workflow function using LLM-powered supervisor

def test_workflow(user_message:str):
    result = supervisor.invoke({"input": user_message})
    # Ensure result is a dict with 'messages' key containing a non-empty list
    if isinstance(result, dict) and "messages" in result:
        messages = result["messages"]
        if isinstance(messages, list) and messages:
            last_message = messages[-1]
            # For objects with .content attribute
            if hasattr(last_message, "content"):
                return last_message.content
            # For dicts with 'content' key
            elif isinstance(last_message, dict) and "content" in last_message:
                return last_message["content"]
    return None
