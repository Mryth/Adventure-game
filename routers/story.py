import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CompleteStoryResponse,CompleteStoryNodeResponse,CreateStoryRequest
)
from schemas.job import StoryJobResponse

router = APIRouter(
    prefixe="/stories",
    tags=["stories"]
)

# it identifies the browser instance using the website or smtg ...
def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model= StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())

    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme="pending"
    )
    db.add(job)
    db.commit()

    # TODO: add background tasks, generate story

def generate_story_task(job_id: str, theme:str, session_id: str):
    db = SessionLocal()
    