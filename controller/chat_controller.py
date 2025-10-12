from fastapi import APIRouter, HTTPException, Request

from dto.ChatRequestDto import ChatTalkRequestDto
from dto.ChatResponseDto import ChatResponseDto
from dto.WorkflowRequestDto import WorkflowRequestDto
from service.workflow_service import WorkflowService

router = APIRouter()
# chatSerivce = chatSerivce()



@router.post("/v1/talk")
async def talk(request: ChatTalkRequestDto)->ChatResponseDto:
    """
    API endpoint to invoke a workflow.

    Expects JSON payload with 'workflow_name', 'user_input', and 'session_id'.
    """
    try:
        # # Invoke the workflow service
        # response = workflow_service.invoke_workflow(
        #     workflow_name=request.workflow_name,
        #     user_input=request.user_input,
        #     session_id=request.session_id
        # )
        print("chat request : ",request)
        return ChatResponseDto(longText="hello", shortText="hi")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "An unexpected error occurred.", "details": str(e)})
