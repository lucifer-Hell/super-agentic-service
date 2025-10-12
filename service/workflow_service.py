from langchain_core.messages import HumanMessage, AIMessage

from workflow.voice_workflow.voice_workflow import voice_workflow
from workflow.voice_workflow.state.voice_state import VoiceState

class WorkflowService:

    def invoke_workflow(self, workflow_name: str, user_input: str, session_id: str):
        """
        Invokes the specified workflow with the given user input and session ID.

        :param workflow_name: Name of the workflow to invoke (e.g., 'voice_workflow').
        :param user_input: The user's input to process.
        :param session_id: The session ID for maintaining state.
        :return: The response from the workflow.
        """
        # Select the workflow to invoke
        if workflow_name == "voice_workflow":
            config = {"configurable": {"thread_id": session_id}}
            response = voice_workflow.invoke({
                "messages": [HumanMessage(content=user_input)],
            }, config=config)
            # Always return the last message in the response
            response : AIMessage = response["messages"][-1]
            return response.content
        else:
            raise ValueError(f"Unknown workflow: {workflow_name}")

        return response
