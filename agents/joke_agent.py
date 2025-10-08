from langgraph.prebuilt import create_react_agent
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

agent = create_react_agent(
    function=joke_agent,
    name="joke_agent",
    description="Tells a random joke to the user."
)

