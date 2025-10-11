from pydantic import BaseModel, Field


class WorkflowRequestDto(BaseModel):
    workflow_name: str = Field(
        description="Workflow name"
    )
    session_id: str = Field(
        description="Session id of the workflow"
    )
    user_input: str = Field(
        description="User input to the workflow"
    )
