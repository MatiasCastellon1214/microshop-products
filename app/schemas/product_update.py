from decimal import Decimal

from pydantic import BaseModel


class ProductUpdate(BaseModel):
    name : str | None = None 
    description : str | None = None 
    price : Decimal | None = None 
    stock : int | None = None