from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import resume_router, chat_router
from app.core.config import settings

app = FastAPI(
    title="TalentScan API",
    description="API for resume parsing and talent search",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume_router.router, prefix="/api", tags=["resume"])
app.include_router(chat_router.router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to TalentScan API"} 