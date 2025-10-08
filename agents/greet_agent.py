from langgraph.prebuilt import create_react_agent

# Greet agent: returns a greeting message

def greet_agent(input_state):
    name = input_state.get('name')
    if name:
        return {"greeting": f"Hello, {name}! Welcome!"}
    else:
        return {"greeting": "Hello! What's your name?"}

agent = create_react_agent(
    function=greet_agent,
    name="greet_agent",
    description="Greets the user. If name is provided, greets by name. Otherwise, asks for name."
)

