from langchain_core.tools import tool

from workflow.test_workflow.state.ivr_state import IVRState

@tool
def register_user(name: str):
    """
    Registers a user's name.

    Args:
        name (str): The name of the user to register.

    Returns:
        dict: A dictionary with the user's name and a flag 'isNamePresent' set to True.
    """
    return {"name": name, "isNamePresent": True}