from uuid import UUID

from sqlmodel import Session, select

from unigate.crud.base import CRUDBase
from unigate.models.feedback_response import FeedbackResponse
from unigate.schemas.feedback_response import FeedbackResponseCreate


class CRUDFeedbackResponse(
    CRUDBase[FeedbackResponse, FeedbackResponseCreate, FeedbackResponseCreate]
):
    def get_by_student_and_question(
        self, session: Session, *, student_id: UUID, group_id: UUID, question_id: str
    ) -> FeedbackResponse | None:
        statement = (
            select(self.model)
            .where(self.model.student_id == student_id)
            .where(self.model.group_id == group_id)
            .where(self.model.question_id == question_id)
        )
        return session.exec(statement).first()

    def get_multi_by_student_and_group(
        self, session: Session, *, student_id: UUID, group_id: UUID
    ) -> list[FeedbackResponse]:
        statement = (
            select(self.model)
            .where(self.model.student_id == student_id)
            .where(self.model.group_id == group_id)
        )
        return session.exec(statement).all()


feedback_response = CRUDFeedbackResponse(FeedbackResponse)