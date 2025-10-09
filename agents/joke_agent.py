import random

# Joke agent: returns a random joke

def joke_agent(input_state):
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the math book look sad? Because it had too many problems.",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ]
    return {"joke": random.choice(jokes)}

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
    name="joke_agent",
    description="Tells a random joke.",
    func=joke_agent
)
