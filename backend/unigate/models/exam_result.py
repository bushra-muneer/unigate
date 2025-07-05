import datetime
import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel  # type: ignore

from unigate.models.base import DBUnigateBase, UUIDBase

if TYPE_CHECKING:
    from unigate.models.student import Student


class ExamResult(DBUnigateBase, UUIDBase, SQLModel, table=True):
    __tablename__ = "exam_results"  # type: ignore

    student_id: uuid.UUID = Field(foreign_key="students.id", nullable=False)
    course_name: str = Field(nullable=False)
    exam_date: datetime.date = Field(nullable=False)
    passed: bool = Field(default=False)
    student: "Student" = Relationship(back_populates="exam_results")
