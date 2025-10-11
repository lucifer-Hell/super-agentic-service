from langgraph.constants import START


voice_workflow = Workflow("VoiceWorkflow")

# Add nodes
short_id_agent = ShortIdAgent(validate_short_id)
qna_agent = QnAAgent(retrieve_data)
ticket_agent = TicketAgent(create_ticket)

voice_workflow.add_node("short_id_agent", short_id_agent)
voice_workflow.add_node("qna_agent", qna_agent)
voice_workflow.add_node("ticket_agent", ticket_agent)

# Define edges
voice_workflow.add_edge(START, "short_id_agent")
voice_workflow.add_conditional_edges(
    "short_id_agent",
    lambda agent_output: agent_output.valid,
    {
        "qna_agent": "qna_agent",
    },
    fallback="short_id_agent"
)
voice_workflow.add_conditional_edges(
    "qna_agent",
    lambda agent_output: agent_output.satisfied,
    {
        END: END,
    },
    fallback="ticket_agent"
)
voice_workflow.add_edge("ticket_agent", END)

# Compile
memory = InMemorySaver()
voice_workflow = voice_workflow.compile(checkpointer=memory)
