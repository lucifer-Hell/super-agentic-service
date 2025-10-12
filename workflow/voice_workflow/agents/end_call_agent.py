from langchain_core.messages import AIMessage

from workflow.voice_workflow.state.voice_state import VoiceState


def end_call_agent_node(state: VoiceState) -> dict:
    return {
        "messages": AIMessage(
            content="Thank you for calling genie. Have a great day!"
        )
    }
