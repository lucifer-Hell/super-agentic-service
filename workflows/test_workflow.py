from commons.agents.router_agent import supervisor

def test_workflow(user_message:str):
    result = supervisor.invoke({
        "messages": [
            {"role": "user", "content": user_message}
        ]
    })
    print(result)
    # Ensure result is a dict with 'messages' key containing a non-empty list
    if isinstance(result, dict) and "messages" in result:
        messages = result["messages"]
        if isinstance(messages, list) and messages:
            # Find the last agent message (joke_agent or greet_agent)
            for msg in reversed(messages):
                if hasattr(msg, "name") and msg.name in ["joke_agent", "greet_agent"]:
                    if hasattr(msg, "content"):
                        return msg.content
                    elif isinstance(msg, dict) and "content" in msg:
                        return msg["content"]
            # Fallback: return last message's content
            last_message = messages[-1]
            if hasattr(last_message, "content"):
                return last_message.content
            elif isinstance(last_message, dict) and "content" in last_message:
                return last_message["content"]
    return None
