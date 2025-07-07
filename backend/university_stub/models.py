# import datetime
# from typing import TYPE_CHECKING
# from sqlmodel import Relationship ,Field, SQLModel # type: ignore
# from unigate.models.base import CourseBase, DBUniBase, UUIDBase, UserBase,ExamBase

# import uuid

# if TYPE_CHECKING:
#     from university_stub.models import Exam
#     from university_stub.models import Student


# class Student(DBUniBase, UUIDBase, UserBase, table=True):
#     __tablename__ = "students"  # type: ignore

#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     number: int = Field(unique=True, index=True, nullable=False)
#     name: str
#     surname: str
#     email: str
#     exam_results: list["ExamResult"] = Relationship(
#         back_populates="student",  # type: ignore
#     )


# class Course(DBUniBase, UUIDBase, CourseBase, table=True):
#     __tablename__ = "courses"  # type: ignore
#     exams: list["Exam"] = Relationship(back_populates="course")


# class Exam(DBUniBase, ExamBase, SQLModel, table=True):
#     __tablename__ = "exams"  # type: ignore

#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     course: "Course" = Relationship(back_populates="exams")



# class ExamResult(DBUniBase, UUIDBase, SQLModel, table=True):
#     __tablename__ = "exam_results"  # type: ignore

#     student_id: uuid.UUID = Field(foreign_key="students.id", nullable=False)
#     course_name: str = Field(nullable=False)
#     exam_date: datetime.date = Field(nullable=False)
#     passed: bool = Field(default=False)
#     student: "Student" = Relationship(back_populates="exam_results")


import datetime
import uuid
from typing import TYPE_CHECKING
from sqlmodel import Relationship, Field, SQLModel  # type: ignore

from unigate.models.base import CourseBase, DBUniBase, UUIDBase, UserBase, ExamBase

if TYPE_CHECKING:
    from university_stub.models import Student, Exam


class Student(DBUniBase, UUIDBase, UserBase, table=True):
    __tablename__ = "students"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    number: int = Field(unique=True, index=True, nullable=False)
    name: str
    surname: str
    email: str

    exam_results: list["ExamResult"] = Relationship(
        back_populates="student",  # type: ignore
    )


class Course(DBUniBase, UUIDBase, CourseBase, table=True):
    __tablename__ = "courses"  # type: ignore

    exams: list["Exam"] = Relationship(back_populates="course")


class Exam(DBUniBase, ExamBase, SQLModel, table=True):
    __tablename__ = "exams"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    course: "Course" = Relationship(back_populates="exams")



class ExamResult(DBUniBase, UUIDBase, SQLModel, table=True):
    __tablename__ = "exam_results"  # type: ignore

    student_id: uuid.UUID = Field(foreign_key="students.id", nullable=False)
    course_name: str = Field(nullable=False)
    exam_date: datetime.date = Field(nullable=False)
    grades_registered_date: datetime.date | None = Field(default=None)
    passed: bool = Field(default=False)

    student: "Student" = Relationship(back_populates="exam_results")

