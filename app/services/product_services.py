

from sqlmodel import Session, col, select

from app.models.Products import Product
from app.schemas.product_create import ProductCreate
from app.schemas.product_update import ProductUpdate


MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 50


class DeduplicateProductError(Exception):
    """Raised when a product with the same name already exists in the database."""


class UnauthorizedProductError(Exception):
    """Raised when a user is not allowed to modify or delete a product."""


def _productname_taken(session: Session, product_name: str, exclude_product_id: int | None = None) -> bool:
    stmt = select(Product.id).where(Product.name == product_name)
    if exclude_product_id is not None:
        stmt = stmt.where(col(Product.id) != exclude_product_id)
    return session.exec(stmt).first() is not None


def create_product(session: Session, data: ProductCreate, owner_id: int | None = None) -> Product:
    if _productname_taken(session, data.name):
        raise DeduplicateProductError("Product name already registered")

    product = Product(
        owner_id=owner_id,
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def list_products(session: Session, skip: int = 0, limit: int = DEFAULT_PAGE_SIZE, owner_id: int | None = None) -> list[Product]:
    capped = min(max(limit, 1), MAX_PAGE_SIZE)
    statement = select(Product)
    if owner_id is not None:
        statement = statement.where(Product.owner_id == owner_id)
    statement = statement.order_by(Product.id).offset(skip).limit(capped)
    return list(session.exec(statement).all())


def get_product_by_id(session: Session, product_id: int) -> Product | None:
    return session.get(Product, product_id)


def update_product(
    session: Session,
    product_id: int,
    data: ProductUpdate,
    current_user_id: int,
) -> Product | None:
    product = session.get(Product, product_id)
    if product is None:
        return None

    if product.owner_id != current_user_id:
        raise UnauthorizedProductError("You are not allowed to update this product.")

    payload = data.model_dump(exclude_unset=True)

    if "name" in payload:
        if _productname_taken(session, payload["name"], exclude_product_id=product_id):
            raise DeduplicateProductError("Product name already registered")

    for key, value in payload.items():
        setattr(product, key, value)

    session.add(product)
    session.commit()
    session.refresh(product)

    return product


def delete_product(session: Session, product_id: int, current_user_id: int) -> bool:
    product = session.get(Product, product_id)
    if product is None:
        return None

    if product.owner_id != current_user_id:
        raise UnauthorizedProductError("You are not allowed to delete this product.")

    session.delete(product)
    session.commit()

    return True
