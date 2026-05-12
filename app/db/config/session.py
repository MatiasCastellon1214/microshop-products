from typing import Generator
from fastapi.params import Depends
from typing_extensions import Annotated

from sqlmodel import Session

from .database import engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
