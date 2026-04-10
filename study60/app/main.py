from fastapi import FastAPI
from src.step01 import router as step1_router
from src.step02 import router as step2_router

app = FastAPI(title="LangChain Ollama Agent API")

# 라우터 등록
app.include_router(step1_router)
app.include_router(step2_router)
