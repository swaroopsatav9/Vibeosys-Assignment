import math
from typing import Tuple, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    """Retrieve a single product by its ID."""
    return db.query(Product).filter(Product.id == product_id).first()


def get_products_paginated(
    db: Session,
    page: int = 1,
    limit: int = 10
) -> Tuple[List[Product], int, int]:
    """
    Retrieve products with pagination.
    Returns: (items, total_records, total_pages)
    """
    total_records = db.query(func.count(Product.id)).scalar() or 0
    total_pages = math.ceil(total_records / limit) if total_records > 0 else 1

    offset = (page - 1) * limit
    items = db.query(Product).order_by(Product.id.asc()).offset(offset).limit(limit).all()

    return items, total_records, total_pages


def create_product(db: Session, product_in: ProductCreate) -> Product:
    """Create a new product in the database."""
    db_product = Product(
        name=product_in.name,
        category=product_in.category,
        description=product_in.description,
        product_image=product_in.product_image,
        sku=product_in.sku,
        unit_of_measure=product_in.unit_of_measure,
        lead_time=product_in.lead_time,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(
    db: Session,
    db_product: Product,
    product_in: ProductUpdate
) -> Product:
    """Update an existing product with provided fields."""
    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, db_product: Product) -> None:
    """Delete a product from the database."""
    db.delete(db_product)
    db.commit()
