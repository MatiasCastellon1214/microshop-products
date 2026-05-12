

from sqlmodel import Session, col, select

from app.models.Products import Product
from app.schemas.product_create import ProductCreate


class DeduplicateProductError(Exception):
    """Raised when a product with the same name already exists in the database."""

def _productname_taken(session: Session, product_name: str, exclude_product_id: int | None = None) -> bool:
    stmt = select(Product.id).where(Product.name == product_name)
    if exclude_product_id is not None:
        stmt = stmt.where(col(Product.id) != exclude_product_id)
    return session.exec(stmt).first() is not None

def create_product(session: Session, data: ProductCreate) -> Product:
    if _productname_taken(session, data.name):
        raise DeduplicateProductError("Product name already registered")

    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock = data.stock
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product