from sqlmodel import SQLModel, create_engine

from app.core.config import get_settings

from app.models.Products import Product

settings = get_settings()
engine = create_engine(
    settings.sqlalchemy_database_uri,
    pool_pre_ping=True,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
