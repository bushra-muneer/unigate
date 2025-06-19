import datetime
from sqlmodel import Session, delete, select

from unigate.crud.base import CRUDBase
from unigate.models.exam_result import ExamResult
from unigate.schemas.exam_result import ExamResultCreate


class CRUDExamResult(CRUDBase[ExamResult, ExamResultCreate, ExamResult]):
    def delete_exam(
        self, *, course_name: str, exam_date: datetime.date, session: Session
    ) -> None:
        session.exec(
            delete(self.model).where(
                self.model.course_name == course_name,
                self.model.exam_date == exam_date,
            )
        )
        session.commit()

    def get_by_exam(
        self, *, course_name: str, exam_date: datetime.date, session: Session
    ) -> list[ExamResult]:
        statement = select(self.model).where(
            self.model.course_name == course_name,
            self.model.exam_date == exam_date,
        )
        return session.exec(statement).all()

exam_result = CRUDExamResult(ExamResult)