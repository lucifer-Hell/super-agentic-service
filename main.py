from fastapi import FastAPI
from controller.workflow_controller import router as workflow_router

app = FastAPI()

# Include the workflow controller routes
app.include_router(workflow_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
