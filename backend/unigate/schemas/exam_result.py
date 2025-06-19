import datetime
import uuid

from pydantic import BaseModel



class ExamResultBase(BaseModel):
    student_id: uuid.UUID
    course_name: str
    exam_date: datetime.date
    passed: bool


class ExamResultCreate(ExamResultBase):
    pass


class ExamResultRead(ExamResultBase):
    id: uuid.UUID