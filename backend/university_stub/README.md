# University API Stub

This service simulates the university backend used by `unigate`.
Data is stored in a PostgreSQL database instead of being generated on the fly.
Set the `UNIVERSITY_DB` environment variable alongside the other
PostgreSQL settings used by `unigate`.

## Running the stub
## Usage

1. Seed the database (only required the first time):
   ```bash
   python -m university_stub.seed_data
   ```
2. Start the stub:
   ```bash
   uvicorn university_stub.main:app --reload --port 8001
   ```

## Endpoints

- `GET /students/{number}` – return a single student.
- `GET /courses` – list all courses.
- `GET /courses/{name}` – details for a specific course.
- `POST /exam-results/query` – get exam results for a course and date.
- `GET /exams/{course}/{date}` – same as above, for compatibility.