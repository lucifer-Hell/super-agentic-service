from fastapi import APIRouter, HTTPException, Request

from dto.WorkflowRequestDto import WorkflowRequestDto
from service.workflow_service import WorkflowService

router = APIRouter()
workflow_service = WorkflowService()



@router.post("/invoke_workflow")
async def invoke_workflow(request: WorkflowRequestDto):
    """
    API endpoint to invoke a workflow.

    Expects JSON payload with 'workflow_name', 'user_input', and 'session_id'.
    """
    try:
        # Invoke the workflow service
        response = workflow_service.invoke_workflow(
            workflow_name=request.workflow_name,
            user_input=request.user_input,
            session_id=request.session_id
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "An unexpected error occurred.", "details": str(e)})
