from langgraph.prebuilt import create_react_agent

# Greet agent: returns a greeting message

def greet_agent(input_state):
    name = input_state.get('name')
    if name:
        return {"greeting": f"Hello, {name}! Welcome!"}
    else:
        return {"greeting": "Hello! What's your name?"}

class SimpleAgent:
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func
    def run(self, input_state):
        return self.func(input_state)
    def invoke(self, input_state):
        return self.run(input_state)

agent = SimpleAgent(
    name="greet_agent",
    description="Greets the user. If name is provided, greets by name. Otherwise, asks for name.",
    func=greet_agent
)
