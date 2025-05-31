from fastapi import APIRouter

from unigate.routes.deps import CurrProfessorDep
from unigate.schemas.course import CourseReadWithUsersAndExams
from sqlmodel import select
from unigate.core.database import SessionDep
from unigate.models import Course, Group,  Student

from sqlmodel import Session
from unigate.routes.deps import SessionDep
from unigate.crud import group as group_crud  



router = APIRouter()


@router.get(
    "/courses",
    response_model=list[CourseReadWithUsersAndExams],
)
def get_courses(current_professor: CurrProfessorDep) -> list[Course]:
    return current_professor.courses

# This endpoint retrieves all courses associated with the current professor,
# excluding any course named "test course". It returns a list of dictionaries
@router.get("/courses-with-groups")
def get_courses_with_groups(
    session: SessionDep,
    current_professor: CurrProfessorDep,
) -> list[dict]:
    results = []
    # Iterate through each course of the current professor
    # and fetch associated groups, excluding "test course"
    for course in current_professor.courses:
        if course.name.strip().lower() == "test course":
            continue  

        print(f"Course: {course.name}")

        # Fetch groups associated with the course
        course_groups: list[Group] = group_crud.get_groups_course(
            session=session, course_name=course.name
        )
        
        print(f"Found {len(course_groups)} groups for course: {course.name}")
        #   Group the course data with its associated groups
        grouped = [
            {
                "id": g.id,
                "name": g.name,
                "type": g.type,
                "date": g.date,
                "description": g.description,
                "examDate": g.exam_date,
                "courseName": course.name,
                "tags": g.tags,
            }
            for g in course_groups
        ]

        results.append({
            "courseId": str(course.id),  
            "courseName": course.name,
            "groups": grouped,
        })
   
    return results
