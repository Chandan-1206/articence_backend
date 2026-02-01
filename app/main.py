from fastapi import FastAPI
from app.routes.calls import router as call_router

app = FastAPI(title="Call Processing Service")

app.include_router(call_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
