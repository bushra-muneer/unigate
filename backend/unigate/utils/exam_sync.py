import httpx

from unigate import crud
from unigate.core.database import get_auth_session, get_session
from unigate.schemas.exam_result import ExamResultCreate


async def sync_exam_results(base_url: str = "http://host.docker.internal:8001") -> None:
    auth_session = next(get_auth_session())
    session = next(get_session())
    async with httpx.AsyncClient(base_url=base_url) as client:
        for course in crud.course.get_all(session=auth_session):
            print(f"Syncing exams for course: {course.name}")
            for exam in course.exams:
                print(f"Exam date: {exam.date}")
                url = f"/exams/{course.name}/{exam.date}"
                print(f"Syncing exam results for {course.name} on {exam.date} from {url}")
                response = await client.get(url)
                print(f"Requesting: {url} => {response.status_code}")
                if response.status_code != 200:
                    continue
                data = response.json()
                crud.exam_result.delete_exam(
                    session=session,
                    course_name=course.name,
                    exam_date=exam.date,
                )
                for number in data["enrolled"]:
                    student = crud.student.get_by_number(number=number, session=session)
                    if not student:
                        continue
                    crud.exam_result.create(
                        session=session,
                        obj_in=ExamResultCreate(
                            student_id=student.id,
                            course_name=course.name,
                            exam_date=exam.date,
                            passed=number in data["passed"],
                        ),
                    )
    auth_session.close()
    session.close()