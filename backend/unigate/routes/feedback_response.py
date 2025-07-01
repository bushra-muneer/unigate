from uuid import UUID

from fastapi import APIRouter, HTTPException

from unigate import crud
from unigate.core.database import SessionDep
from unigate.models.feedback_response import FeedbackResponse
from unigate.schemas.feedback_response import (
    FeedbackResponseCreate,
    FeedbackResponseRead,
)

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/response", response_model=FeedbackResponseRead)
def submit_response(
    session: SessionDep, data: FeedbackResponseCreate
) -> FeedbackResponse:
    """
    Submit a single feedback response.
    If a response for this student, group, and question already exists,
    it returns the existing one. Otherwise, it creates a new one.
    """
    existing_response = crud.feedback_response.get_by_student_and_question(
        session=session,
        student_id=data.student_id,
        group_id=data.group_id,
        question_id=data.question_id,
    )
    if existing_response:
        # Ответы неизменяемы, просто возвращаем существующий
        return existing_response

    # Если ответа нет, создаем новый
    return crud.feedback_response.create(session=session, obj_in=data)


@router.get("/responses", response_model=list[FeedbackResponseRead])
def get_student_responses_for_group(
    session: SessionDep, student_id: UUID, group_id: UUID
) -> list[FeedbackResponse]:
    """
    Get all feedback responses for a specific student in a specific group.
    """
    return crud.feedback_response.get_multi_by_student_and_group(
        session=session, student_id=student_id, group_id=group_id
    )