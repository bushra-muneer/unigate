from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import date

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
    existing_response = crud.feedback_response.get_by_student_and_question(
        session=session,
        student_id=data.student_id,
        group_id=data.group_id,
        question_id=data.question_id,
    )
    if existing_response:
        return existing_response

    return crud.feedback_response.create(session=session, obj_in=data)


@router.get("/responses", response_model=list[FeedbackResponseRead])
def get_student_responses_for_group(
    session: SessionDep, student_id: UUID, group_id: UUID
) -> list[FeedbackResponse]:
    return crud.feedback_response.get_multi_by_student_and_group(
        session=session, student_id=student_id, group_id=group_id
    )


@router.get("/helpfulness-distribution")
def helpfulness_distribution(
    session: SessionDep,
    exam_date: Optional[date] = Query(None),
):
    """
    Returns percentage breakdown of Helpful / Not Helpful / Not Answered 
    grouped by group size (2–5, 6–10, 11–20, 21–50).
    """

    # Step 1: Get size per group_id
    size_by_group = {}
    size_query = session.query(FeedbackResponse).filter(
        FeedbackResponse.question_id == "bestSize"
    )
    if exam_date:
        size_query = size_query.filter(FeedbackResponse.exam_date == exam_date)

    for size_response in size_query.all():
        size_by_group[size_response.group_id] = size_response.answer  # e.g., "2–5"

    # Step 2: Define group buckets
    stats = {
        "2–5": {"helpful": 0, "not_helpful": 0, "not_answered": 0, "total": 0},
        "6–10": {"helpful": 0, "not_helpful": 0, "not_answered": 0, "total": 0},
        "11–20": {"helpful": 0, "not_helpful": 0, "not_answered": 0, "total": 0},
        "21–50": {"helpful": 0, "not_helpful": 0, "not_answered": 0, "total": 0},
    }

    # Step 3: Get helpful responses
    helpful_query = session.query(FeedbackResponse).filter(
        FeedbackResponse.question_id == "helpful"
    )
    if exam_date:
        helpful_query = helpful_query.filter(FeedbackResponse.exam_date == exam_date)

    for response in helpful_query.all():
        group_size = size_by_group.get(response.group_id)
        if not group_size or group_size not in stats:
            continue  # skip if no size data or invalid bucket

        if response.answer is True:
            stats[group_size]["helpful"] += 1
        elif response.answer is False:
            stats[group_size]["not_helpful"] += 1
        else:
            stats[group_size]["not_answered"] += 1

        stats[group_size]["total"] += 1

    # Step 4: Format result
    result = []
    for size, counts in stats.items():
        total = counts["total"]
        if total == 0:
            continue
        result.append({
            "group_size": size,
            "helpful_pct": round(100 * counts["helpful"] / total, 1),
            "not_helpful_pct": round(100 * counts["not_helpful"] / total, 1),
            "not_answered_pct": round(100 * counts["not_answered"] / total, 1),
        })
    return result

