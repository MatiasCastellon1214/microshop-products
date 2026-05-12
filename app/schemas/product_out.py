from decimal import Decimal
from pydantic import BaseModel

class ProductOut(BaseModel):
    id: int
    name: str
    description : str | None = None 
    price : Decimal 
    stock: int

    model_config = {"from_attributes": True}