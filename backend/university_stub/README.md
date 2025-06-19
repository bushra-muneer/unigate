+21-0
# University API Stub

This minimal FastAPI application emulates the university system so that the backend can fetch
student and course data without relying on the real service.

## Running the stub

From the `backend/university_stub` directory run:

```bash
uvicorn main:app --reload --port 8001
```

The stub exposes the following endpoints:

<!-- - `GET /students/{number}` — return basic student information.
- `GET /courses` — list all courses.
- `GET /courses/{name}` — details for a specific course. -->
- `GET /exams/{course}/{date}` — enrolled and passed students for an exam date.

The daa returned is static and only intended for testing purposes.