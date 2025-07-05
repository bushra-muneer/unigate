from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import (
    Session,  # type: ignore
    create_engine,
    text,  # type: ignore
)

# Import models to register them
from unigate import models  # makes sure model classes are loaded

from unigate.models.base import DBUnigateBase, DBAuthBase, DBUniBase  # <-- IMPORTANT: use the custom registry
from unigate.core.config import settings

# Create the database engines
engine = create_engine(str(settings.UNIGATE_DB_URI))
auth_engine = create_engine(str(settings.AUTH_DB_URI))
uniStub_engine = create_engine(str(settings.UNISTUB_DB_URI))


# Use the correct metadata registry
def init_db() -> None:
    DBUnigateBase.metadata.create_all(engine)
    DBAuthBase.metadata.create_all(auth_engine)
    DBUniBase.metadata.create_all(uniStub_engine)

# Dependency-injected sessions
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def get_auth_session() -> Generator[Session, None, None]:
    with Session(auth_engine) as session:
        yield session

def get_unistub_session() -> Generator[Session, None, None]:
    """Return a session bound to the University stub database."""
    with Session(uniStub_engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
AuthSessionDep = Annotated[Session, Depends(get_auth_session)]
UniStubSessionDep = Annotated[Session, Depends(get_unistub_session)]


if __name__ == "__main__":
    print("Initializing databases...")
    init_db()
    print("✅ Done.")
