from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .agent import process_request


app = FastAPI(
    title="AINIOS Airline Resolution Agent",
    description="Customer-facing airline disruption resolution agent",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResolutionRequest(BaseModel):
    pnr: str
    message: str


@app.get("/")
def root():
    return {
        "message": "AINIOS Airline Resolution Agent API",
        "status": "running"
    }


@app.post("/api/resolve")
def resolve(request: ResolutionRequest):

    return process_request(
        request.pnr,
        request.message
    )