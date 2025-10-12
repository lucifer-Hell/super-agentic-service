from workflow.test_workflow.state.ivr_state import IVRState


def router_agent(state:IVRState):
    """Route to the appropriate agent based on the state."""
    print("current state ",state)
    if not state.isNamePresent:
        print("routing to : user_info_agent")
        return {"call_agent":"user_info_agent"}
    else:
        print("routing to : joke_agent")
        return {"call_agent":"joke_agent"}