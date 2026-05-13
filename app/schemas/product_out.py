from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from sqlmodel import Field

from app.models.Products import _utc_now

class ProductOut(BaseModel):
    id: int
    name: str
    description : str | None = None 
    price : Decimal 
    stock: int
    created_at :  datetime = Field(default_factory=_utc_now)

    model_config = {"from_attributes": True}