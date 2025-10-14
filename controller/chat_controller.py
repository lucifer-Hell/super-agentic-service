from fastapi import APIRouter, HTTPException, Request

from dto.ChatRequestDto import ChatTalkRequestDto
from dto.ChatResponseDto import ChatResponseDto
from dto.WorkflowRequestDto import WorkflowRequestDto
from service.workflow_service import WorkflowService

router = APIRouter()
workFlowService = WorkflowService()


@router.post("/v1/talk")
async def talk(request: ChatTalkRequestDto)->ChatResponseDto:
    """
    API endpoint to invoke a workflow.

    Expects JSON payload with 'workflow_name', 'user_input', and 'session_id'.
    """
    response=""
    try:
        response =  workFlowService.invoke_workflow(
            workflow_name=request.requestAttributes.flows.entry.ref,
            user_input= request.message.query,
            session_id=request.conversationId
        )
        return ChatResponseDto(longText=response,shortText=response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "An unexpected error occurred.", "details": str(e)})



@router.get("/health")
def health_check():
    """ Health check endpoint """
    return {"status": "ok"}