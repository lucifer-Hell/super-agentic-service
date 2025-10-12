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
        if request.requestAttributes.flows.entry.ref.lower() == 'ivr_workflow':
            response =  workFlowService.invoke_workflow(
                workflow_name='ivr_workflow',
                user_input= request.message.query,
                session_id=request.conversationId
            )
        elif  request.requestAttributes.flows.entry.ref.lower() == 'chat_workflow':
            response =  workFlowService.invoke_workflow(
                workflow_name='chat_workflow',
                user_input= request.message.query,
                session_id=request.conversationId
            )
        # TODO HANDLE THIS PROPERLY
        return ChatResponseDto(longText=response,shortText=response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "An unexpected error occurred.", "details": str(e)})
