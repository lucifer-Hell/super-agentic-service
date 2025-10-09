import llm_providers.openai_llm as openai_llm
from agents.greet_agent import agent as greet_agent
from agents.joke_agent import agent as joke_agent


from langgraph_supervisor import create_supervisor

supervisor = create_supervisor(
    model=openai_llm.llm,
    agents=[greet_agent, joke_agent],
    prompt=(
        "You are a supervisor. Based on the user message, you must call ONE of the following agents:\n"
        "- joke agent: Use for any request for a joke, humor, something funny, or to make the user laugh. Example requests: 'tell me a joke', 'make me laugh', 'say something funny', 'I want to hear a joke', 'give me a joke'.\n"
        "- greet agent: Use for any greeting, pleasantries, or social niceties. Example requests: 'say hello', 'how are you?', 'good morning', 'hello', 'hi', 'greetings'.\n"
        "Assign work to one agent at a time. Do not call agents in parallel.\n"
        "Do not do any work yourself.\n"
        "Do not ask questions back to the user.\n"
        "If you are not sure, make your best guess. If the user asks for a joke, humor, or something funny, always call the joke agent.\n"
        "User input: {input}\n"
    ),
    add_handoff_back_messages=False,
).compile()