
from collections.abc import Sequence
from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from unigate.core.database import get_session
from .models import Course, Exam, ExamResult, Student

app = FastAPI(title="University Stub")

# @app.on_event("startup")
# def on_startup() -> None:
#     init_db()


@app.get("/stub/students/{number}", response_model=Student)
def get_student(number: int, session: Session = Depends(get_session)) -> Student:
    student = session.exec(select(Student).where(Student.number == number)).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/stub/courses", response_model=list[Course])
def list_courses(session: Session = Depends(get_session)) -> Sequence[Course]:
    """List all courses."""
    try:
        courses = session.exec(select(Course)).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return courses

@app.get("/stub/courses/{name}", response_model=Course)
def get_course(name: str, session: Session = Depends(get_session)) -> Course:
    course = session.exec(select(Course).where(Course.name == name)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.post("/stub/exam-results/query", response_model=list[ExamResult])
def query_results(
    course: str,
    exam_date: date,
    session: Session = Depends(get_session),
) -> list[ExamResult]:
    exam = session.exec(
        select(Exam)
        .where(Exam.date == exam_date)
        .join(Course)
        .where(Course.name == course)
    ).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return session.exec(select(ExamResult).where(ExamResult.exam_id == exam.id)).all()


@app.get("/stub/exams/{course}/{exam_date}", response_model=list[ExamResult])
def get_exam_result(
    course: str, exam_date: str, session: Session = Depends(get_session)
) -> list[ExamResult]:
    try:
        parsed_date = date.fromisoformat(exam_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    return query_results(course, parsed_date, session)


if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8001)
    uvicorn.run(app, host="localhost", port=8090)
