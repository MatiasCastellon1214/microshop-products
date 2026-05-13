
from fastapi.params import Query
from typing import Optional
from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Response, status, HTTPException
from app.core.auth import CurrentUser, get_current_user
from app.db.config.session import SessionDep
from app.schemas.product_create import ProductCreate
from app.schemas.product_out import ProductOut
from app.schemas.product_update import ProductUpdate
from app.services.product_services import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    DeduplicateProductError,
    UnauthorizedProductError,
    create_product,
    delete_product,
    get_product_by_id,
    list_products,
    update_product,
)

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product_route(
    body: ProductCreate,
    session: SessionDep,
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        return create_product(session, body, owner_id=current_user.id)
    except DeduplicateProductError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get("", response_model=list[ProductOut])
def list_product_route(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0, description="Rows to skip")] = 0,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=MAX_PAGE_SIZE,
            description=f"Page size (max {MAX_PAGE_SIZE})",
        ),
    ] = DEFAULT_PAGE_SIZE,
    owner_id: Optional[int] = Query(default=None, description="Filter by owner id"),
):
    return list_products(session, skip=skip, limit=limit, owner_id=owner_id)


@router.get("/{product_id}", response_model=ProductOut)
def get_product_route(
    product_id: int,
    session: SessionDep,
):
    product = get_product_by_id(session, product_id)
    if product is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.patch("/{product_id}", response_model=ProductOut)
def update_product_route(
    product_id: int,
    body: ProductUpdate,
    session: SessionDep,
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        product = update_product(session, product_id, body, current_user.id)
    except DeduplicateProductError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except UnauthorizedProductError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_route(
    product_id: int,
    session: SessionDep,
    current_user: CurrentUser = Depends(get_current_user),
):
    product = get_product_by_id(session, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    delete_product(session, product_id, current_user.id)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)