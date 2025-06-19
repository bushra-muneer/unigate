from fastapi import FastAPI, HTTPException
from datetime import date
from pydantic import BaseModel
import random

app = FastAPI(title="University Stub")

class Student(BaseModel):
    number: int
    name: str
    surname: str
    email: str

class Course(BaseModel):
    name: str
    exams: list[date]

class ExamResult(BaseModel):
    course: str
    date: date
    enrolled: list[int]
    passed: list[int]

# Students
students = {
    1234567: Student(
        number=1234567,
        name="Test",
        surname="Student",
        email="s1234567@studenti.unige.it",
    ),
    4891185: Student(
        number=4891185,
        name="Fabio",
        surname="Fontana",
        email="s4891185@studenti.unige.it",
    ),
    4989646: Student(
        number=4989646,
        name="Lorenzo",
        surname="Foschi",
        email="s4989646@studenti.unige.it",
    ),
}
#real seed works fine --> for base seed you have random exam dates for each course
# this is dummy data which we get from university 
# Courses with all requested exam dates
courses = {
    "Test Course": Course(
        name="Test Course",
        exams=[date(2025, 1, 1), date(2025, 1, 25)]
    ),
    "Binary Analysis and secure coding": Course(
        name="Binary Analysis and secure coding",
        exams=[date(2025, 1, 8), date(2025, 2, 10)]
    ),
    "Capstone": Course(
        name="Capstone",
        exams=[date(2025, 2, 3), date(2025, 2, 17)]
    ),
    "Decentralized Systems": Course(
        name="Decentralized Systems",
        exams=[date(2025, 1, 14), date(2025, 2, 13)]
    ),
    "High Performance Computing": Course(
        name="High Performance Computing",
        exams=[date(2025, 1, 21), date(2025, 2, 18)]
    ),
    "Machine Learning": Course(
        name="Machine Learning",
        exams=[date(2025, 1, 20), date(2025, 2, 19)]
    ),
    "Network Security": Course(
        name="Network Security",
        exams=[date(2025, 1, 27), date(2025, 2, 20)]
    ),
    "Digital Forensics": Course(
        name="Digital Forensics",
        exams=[date(2025, 1, 28), date(2025, 2, 21)]
    ),
    "Virtualization and Cloud Computing": Course(
        name="Virtualization and Cloud Computing",
        exams=[date(2025, 2, 4), date(2025, 2, 26)]
    ),
    "Data Protection and Privacy": Course(
        name="Data Protection and Privacy",
        exams=[date(2025, 2, 11), date(2025, 2, 27)]
    )
}

@app.get("/students/{number}", response_model=Student)
async def get_student(number: int) -> Student:
    student = students.get(number)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/courses", response_model=list[Course])
async def list_courses() -> list[Course]:
    return list(courses.values())

@app.get("/courses/{name}", response_model=Course)
async def get_course(name: str) -> Course:
    course = courses.get(name)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.get("/exams/{course}/{exam_date}", response_model=ExamResult)
async def get_exam_result(course: str, exam_date: str) -> ExamResult:
    try:
        parsed_date = date.fromisoformat(exam_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    course_obj = courses.get(course)
    if not course_obj:
        raise HTTPException(status_code=404, detail="Course not found")

    if parsed_date not in course_obj.exams:
        raise HTTPException(status_code=404, detail="Exam date not found for this course")

    # Generate enrolled and passed lists dynamically
    student_numbers = list(students.keys())
    num_enrolled = random.randint(2, len(student_numbers))  # At least 2 enrolled
    enrolled = random.sample(student_numbers, num_enrolled)
    num_passed = random.randint(0, len(enrolled))  # Any subset could pass
    passed = random.sample(enrolled, num_passed)

    return ExamResult(
        course=course,
        date=parsed_date,
        enrolled=enrolled,
        passed=passed
    )
