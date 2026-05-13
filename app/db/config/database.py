from sqlmodel import SQLModel, create_engine

from app.core.config import get_settings

from app.models.Products import Product

settings = get_settings()

print("JWT_SECRET:", settings.jwt_secret)
print("JWT_ALGORITHM:", settings.jwt_algorithm)
print("DATABASE_URL:", settings.database_url)

engine = create_engine(
    settings.sqlalchemy_database_uri,
    pool_pre_ping=True,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
