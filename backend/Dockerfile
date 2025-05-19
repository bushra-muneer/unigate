
FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.9 /uv /bin/uv

# Virtual environment path
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_HTTP_TIMEOUT=300

# Copy dependency files early for caching
COPY ./pyproject.toml ./uv.lock /app/

# Install dependencies (initial sync without project install)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy remaining source files
COPY ./unigate /app/unigate
COPY ./alembic_unigate /app/alembic_unigate
COPY ./alembic_auth /app/alembic_auth
COPY ./seeders /app/seeders

# Final sync (with project install)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Start FastAPI server
CMD ["fastapi", "run", "--reload", "unigate/main.py"]
