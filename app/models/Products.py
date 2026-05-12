from datetime import datetime, timezone
from decimal import Decimal
from sqlmodel import Field, SQLModel

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Product(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str = Field(index=True, unique=True)
    description : str | None = Field(index=True)
    price : Decimal = Field(default=0.0)
    stock : int = Field(default=0)
    created_at :  datetime = Field(default_factory=_utc_now)