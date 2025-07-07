
from collections.abc import Sequence
from datetime import date
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from unigate.core.database import get_unistub_session
from .models import Course, Exam, ExamResult, Student

from fastapi import APIRouter, Body, Query

app = FastAPI(title="University Stub")

# @app.on_event("startup")
# def on_startup() -> None:
#     init_db()


@app.get("/stub/students/{number}", response_model=Student)
def get_student(number: int, session: Session = Depends(get_unistub_session)) -> Student:
    student = session.exec(select(Student).where(Student.number == number)).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/stub/courses", response_model=list[Course])
def list_courses(session: Session = Depends(get_unistub_session)) -> Sequence[Course]:
    """List all courses."""
    try:
        courses = session.exec(select(Course)).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return courses

@app.get("/stub/courses/{name}", response_model=Course)
def get_course(name: str, session: Session = Depends(get_unistub_session)) -> Course:
    course = session.exec(select(Course).where(Course.name == name)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.post("/stub/exam-results/query", response_model=list[ExamResult])
def query_results(
    course: str,
    exam_date: date,
    session: Session = Depends(get_unistub_session),
) -> list[ExamResult]:
    exam = session.exec(
        select(Exam)
        .where(Exam.date == exam_date)
        .join(Course)
        .where(Course.name == course)
    ).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return session.exec(
        select(ExamResult)
        .where(ExamResult.course_name == course)
        .where(ExamResult.exam_date == exam_date)
    ).all()


@app.get("/stub/exams/{course}/{exam_date}", response_model=list[ExamResult])
def get_exam_result(
    course: str, exam_date: str, session: Session = Depends(get_unistub_session)
) -> list[ExamResult]:
    try:
        parsed_date = date.fromisoformat(exam_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    return query_results(course, parsed_date, session)


@app.post("/stub/exam-results/pass-count")
def count_passed(
    course: str = Query(..., description="Course name"),
    start_date: date = Query(..., description="Start of date range"),
    end_date: date = Query(..., description="End of date range"),
    student_numbers: List[int] = Body(..., embed=True),
    session: Session = Depends(get_unistub_session),
) -> dict:
    """Return the number of students who passed a course within a date range and their student numbers."""

    if start_date > end_date:
        raise HTTPException(
            status_code=400, detail="start_date must be before end_date"
        )

    if not student_numbers:
        return {"count": 0, "passed_ids": []}

    # Fetch student records for given numbers
    students = session.exec(
        select(Student).where(Student.number.in_(student_numbers))
    ).all()

    if not students:
        return {"count": 0, "passed_ids": []}

    student_id_to_number = {s.id: s.number for s in students}
    student_ids = list(student_id_to_number.keys())

    # Fetch passed exam results
    results = session.exec(
        select(ExamResult.student_id)
        .where(ExamResult.student_id.in_(student_ids))
        .where(ExamResult.course_name == course)
        .where(ExamResult.exam_date.between(start_date, end_date))
        .where(ExamResult.passed.is_(True))
    ).unique().all()

    # Map student UUIDs back to student numbers
    passed_numbers = [student_id_to_number[res] for res in results if res in student_id_to_number]

    return {
        "count": len(passed_numbers),
        "passed_ids": passed_numbers
    }


@app.post("/stub/exam-results/passed-in-attempt")
def get_passed_students_in_attempt(
    course: str = Query(..., description="Course name (e.g., Capstone)"),
    exam_date: date = Query(..., description="Exam date of attempt 1 (e.g., 2025-06-06)"),
    next_attempt_date: date = Query(..., description="Exam date of next attempt (e.g., 2025-07-13)"),
    student_numbers: List[int] = Body(..., embed=True),
    session: Session = Depends(get_unistub_session),
) -> dict:
    """
    Return student numbers who passed a specific exam date and had grades registered before the next attempt.
    """

    if not student_numbers:
        return {"count": 0, "passed_ids": []}

    # Fetch students from the given numbers
    students = session.exec(
        select(Student).where(Student.number.in_(student_numbers))
    ).all()

    if not students:
        return {"count": 0, "passed_ids": []}

    student_id_map = {s.id: s.number for s in students}
    student_ids = list(student_id_map.keys())

    # Fetch exam results matching the criteria
    results = session.exec(
        select(ExamResult.student_id)
        .where(ExamResult.student_id.in_(student_ids))
        .where(ExamResult.course_name == course)
        .where(ExamResult.exam_date == exam_date)
        .where(ExamResult.grades_registered_date != None)
        .where(ExamResult.grades_registered_date < next_attempt_date)
        .where(ExamResult.passed.is_(True))
    ).all()

    # Convert UUIDs to student numbers
    passed_numbers = [student_id_map[student_id] for student_id in results if student_id in student_id_map]

    return {
        "count": len(passed_numbers),
        "passed_ids": passed_numbers
    }


if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8001)
    uvicorn.run(app, host="localhost", port=8090)
