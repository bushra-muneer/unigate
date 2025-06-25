from datetime import datetime
from typing import ClassVar
from uuid import UUID

from sqlmodel import Field

from unigate.models.base import DBUnigateBase, UUIDBase


class FeedbackResponse(DBUnigateBase, UUIDBase, table=True):
    # Эта строка исправлена
    tablename: ClassVar[str] = "feedback_responses"

    student_id: UUID = Field(foreign_key="students.id", index=True, nullable=False)
    group_id: UUID = Field(foreign_key="groups.id", index=True, nullable=False)
    question_id: str = Field(nullable=False)
    answer: str = Field(nullable=False)
    exam_date: datetime = Field(nullable=False)