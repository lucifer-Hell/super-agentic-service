from langchain_core.tools import tool

from workflows.ivr_workflow.state.ivr_state import IVRState


@tool
def register_user(state:IVRState, name: str):
    """Register the user's name in the state."""
    state.name = name
    state.isNamePresent = True
    return f"User name '{name}' registered successfully."