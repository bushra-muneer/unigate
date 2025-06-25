from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class FeedbackResponseBase(BaseModel):
    student_id: UUID
    group_id: UUID
    question_id: str
    answer: str
    exam_date: date 


class FeedbackResponseCreate(FeedbackResponseBase):
    pass


class FeedbackResponseRead(FeedbackResponseBase):
    id: UUID