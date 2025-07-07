
import random
from datetime import datetime, date, timedelta

import pytz
from sqlmodel import select, Session

from unigate.utils.exam_sync import sync_exam_results
from unigate import crud
from unigate.core.database import (
    get_auth_session,
    get_session,
)
from unigate.core.database import (
    uniStub_engine as engine,
)
from unigate.core.security import get_password_hash
from unigate.enums import GroupType
from unigate.models.course import Course
from unigate.models.exam import Exam
from unigate.models.exam_result import ExamResult
from unigate.models.student import Student
from unigate.models.teach import Teach
from unigate.schemas.auth import AuthUserCreate
from unigate.schemas.course import CourseCreate
from unigate.schemas.group import GroupCreate
from unigate.schemas.student import StudentCreate



from university_stub.models import (
    Course as UniStubCourse,
)
from university_stub.models import (
    Exam as UniStubExam,
)
from university_stub.models import (
    ExamResult as UniStubExamResult,
)
from university_stub.models import (
    Student as UniStubStudent,
)


# ------------------------ Data Setup ------------------------

students = [
    StudentCreate(
        number=1234567,
        email="s1234567@studenti.unige.it",
        name="Test Name",
        surname="Test Surname",
    ),
    StudentCreate(
        number=4891185,
        email="s4891185@studenti.unige.it",
        name="Fabio",
        surname="Fontana",
    ),
    StudentCreate(
        number=4989646,
        email="s4989646@studenti.unige.it",
        name="Lorenzo",
        surname="Foschi",
    ),
    StudentCreate(
        number=5806782,
        email="s5806782@studenti.unige.it",
        name="Mimmo",
        surname="Torabi",
    ),
    StudentCreate(
        number=6015033, email="s6015033@studenti.unige.it", name="Musse", surname="Gher"
    ),
    StudentCreate(
        number=4820312,
        email="s4820312@studenti.unige.it",
        name="Giovanni",
        surname="Bosi",
    ),
    StudentCreate(
        number=5475593,
        email="s5475593@studenti.unige.it",
        name="Forough",
        surname="Majidi",
    ),
    StudentCreate(
        number=4878744,
        email="s4878744@studenti.unige.it",
        name="Michele",
        surname="Frattini",
    ),
    ]

professors = [
        AuthUserCreate(
        number=0,
        email="test@unige.it",
        name="Test Name",
        surname="Test Surname",
        hashed_password=get_password_hash("testpassword"),
    ),
    AuthUserCreate(
        number=1000000,
        email="marina.ribaudo@unige.it",
        name="Marina",
        surname="Ribaudo",
        hashed_password=get_password_hash("testpassword"),
    ),
    AuthUserCreate(
        number=2000000,
        email="maura.cerioli@unige.it",
        name="Maura",
        surname="Cerioli",
        hashed_password=get_password_hash("testpassword"),
    ),
    AuthUserCreate(
        number=3000000,
        email="matteo.dellamico@unige.it",
        name="Matteo",
        surname="Dell'Amico",
        hashed_password=get_password_hash("testpassword"),
    ),
    AuthUserCreate(
        number=4000000,
        email="s6180175@studenti.unige.it",
        name="Bushra",
        surname="Muneer",
        hashed_password=get_password_hash("testpassword"),
    ),
    ]

groups = [
   
   GroupCreate(
        name="Test Public Group",
        description="This is a test group",
        category="Test",
        type=GroupType.PUBLIC,
        course_name="Test Course",
        date=datetime(2025, 1, 1, tzinfo=pytz.utc),
        exam_date=datetime(2025, 1, 1, tzinfo=pytz.utc),
    ),
    GroupCreate(
        name="Test Public Group",
        description="This is a test group",
        category="Test",
        type=GroupType.PUBLIC,
        course_name="Test Course",
        date=datetime(2025, 2, 2, tzinfo=pytz.utc),
        exam_date=datetime(2025, 2, 2, tzinfo=pytz.utc),
    ),
    GroupCreate(
        name="Test Private Group",
        description="This is a test group",
        category="Test",
        type=GroupType.PRIVATE,
        course_name="Test Course",
        date=datetime(2025, 1, 1, tzinfo=pytz.utc),
        exam_date=datetime(2025, 1, 1, tzinfo=pytz.utc),
    ),
   ]

courses = {
    "Test Course": {
        "course": CourseCreate(name="Test Course"),
        "professors": [professors[0], professors[3], professors[4]],
        "exam_dates": [datetime(2025, 1, 1, tzinfo=pytz.utc)],
    },
    "Capstone": {
        "course": CourseCreate(name="Capstone"),
        "professors": [professors[1], professors[2], professors[4]],
        "exam_dates": [],
    },
    "Distributed Systems": {
        "course": CourseCreate(name="Distributed Systems"),
        "professors": [professors[1], professors[3], professors[4]],
        "exam_dates": [],
    },
}

# Generate random exam dates for Jan, Feb, June, July, Sept
def generate_exam_dates()-> list[datetime]:
    months = [1, 2, 6, 7, 9]
    #return [datetime(2025, month, random.randint(1, 28), tzinfo=pytz.utc) for month in months]
    return [
            datetime(2025, month, random.randint(1, 28), tzinfo=pytz.utc)  # noqa: S311
            for month in months
        ]
for course_name, details in courses.items():
    if course_name != "Test Course":
        details["exam_dates"] = generate_exam_dates()

users = professors + [
    AuthUserCreate.model_validate(
        student, update={"hashed_password": get_password_hash("testpassword")}
    )
    for student in students
]

# ------------------------ Seeder Functions ------------------------

def seed_auth() -> None:
    session = next(get_auth_session())
    created_courses = {}

    for course_name, details in courses.items():
        created_course = Course(name=details["course"].name)
        session.add(created_course)
        created_courses[course_name] = created_course

        for exam_date in details["exam_dates"]:
            session.add(Exam(course_id=created_course.id, date=exam_date))

    for user in users:
        created_user = crud.auth_user.create(obj_in=user, session=session)
        if user in professors:
            for course_name, details in courses.items():
                if user in details["professors"]:
                    session.add(
                        Teach(
                            professor_id=created_user.id,
                            course_id=created_courses[course_name].id,
                        )
                    )
    session.commit()

def seed_unigate() -> None:
    session = next(get_session())

    for student in students:
        current_student = crud.student.create(obj_in=student, session=session)
        for group in groups:
            current_group = crud.group.create(
                obj_in=group,
                update={
                    "creator_id": current_student.id,
                    "name": f"Test {student.number} {group.type.value}",
                    "course_name": group.course_name,
                    "exam_date": group.exam_date,
                },
                session=session,
            )
            current_group.students.append(current_student)
            current_group.super_students.append(current_student)
            session.add(current_group)
            session.commit()

# ------------------------ University Stub Seeder ------------------------
def seed_unistub() -> None:
    with Session(engine) as session:  # type: ignore
        if session.exec(select(UniStubStudent)).first():
            return

        # Add students
        students = [
            UniStubStudent(
                number=4891185,
                name="Fabio",
                surname="Fontana",
                email="s4891185@studenti.unige.it",
            ),
            UniStubStudent(
                number=4989646,
                name="Lorenzo",
                surname="Foschi",
                email="s4989646@studenti.unige.it",
            ),
        ]
        for student in students:
            session.add(student)
        session.commit()

        # Add courses
        courses = [
            UniStubCourse(name="Distributed Systems"),
            UniStubCourse(name="Capstone"),
        ]
        for course in courses:
            session.add(course)
        session.commit()

        # Refresh course IDs
        session.refresh(courses[0])
        session.refresh(courses[1])

        # Define exam dates
        course_exam_map = {
            "Distributed Systems": [date(2025, 1, 11), date(2025, 2, 8)],
            "Capstone": [date(2025, 6, 6), date(2025, 7, 13), date(2025, 9, 11)],
        }

        # Add exams and conditionally update/insert results
        for course in courses:
            for exam_date in course_exam_map[course.name]:
                exam = UniStubExam(course_id=course.id, date=exam_date)
                session.add(exam)
                session.commit()
                session.refresh(exam)

                for i, student in enumerate(students):
                    # Define passed status and grade registration date
                    passed = (i % 2 == 0)
                    grade_date = exam.date + timedelta(days=7)

                    # Check if result for this student+course already exists
                    existing_result = session.exec(
                        select(UniStubExamResult)
                        .where(UniStubExamResult.student_id == student.id)
                        .where(UniStubExamResult.course_name == course.name)
                    ).first()

                    if existing_result:
                        # Update the existing result
                        existing_result.exam_date = exam.date
                        existing_result.grades_registered_date = grade_date
                        existing_result.passed = passed
                        session.add(existing_result)
                    else:
                        # Insert new result
                        result = UniStubExamResult(
                            student_id=student.id,
                            course_name=course.name,
                            exam_date=exam.date,
                            grades_registered_date=grade_date,
                            passed=passed,
                        )
                        session.add(result)
        session.commit()



# ------------------------ Entrypoint ------------------------

if __name__ == "__main__":
    seed_auth()
    seed_unigate()
    seed_unistub()

    # import asyncio
    # asyncio.run(sync_exam_results())
