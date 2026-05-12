
from fastapi import APIRouter, status, HTTPException
from app.db.config.session import SessionDep
from app.schemas.product_create import ProductCreate
from app.schemas.product_out import ProductOut
from app.services.product_services import (
    DeduplicateProductError,
    create_product
)

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model= ProductOut, status_code= status.HTTP_201_CREATED)
def create_product_route(body: ProductCreate, sesssion:SessionDep):
    try:
        return create_product(sesssion, body)
    except DeduplicateProductError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        ) from exc
    

