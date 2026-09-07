from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import product as crud_product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductPaginationResponse,
    MessageResponse,
)

router = APIRouter(prefix="/product", tags=["Products"])


@router.get(
    "/list",
    response_model=ProductPaginationResponse,
    summary="List all products with pagination",
    description="Retrieve a paginated list of products with 10 records per page by default."
)
def list_products(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page (default: 10)"),
    db: Session = Depends(get_db)
):
    """
    List all products with pagination.
    - **page**: Page number (default: 1)
    - **limit**: Records per page (default: 10)
    """
    items, total_records, total_pages = crud_product.get_products_paginated(
        db=db, page=page, limit=limit
    )

    return ProductPaginationResponse(
        items=items,
        total_records=total_records,
        current_page=page,
        page_size=limit,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )


@router.get(
    "/{pid}/info",
    response_model=ProductResponse,
    summary="View product information",
    description="View detailed information about a product by its ID."
)
def get_product_info(
    pid: int = Path(..., ge=1, description="Unique Product ID"),
    db: Session = Depends(get_db)
):
    """
    Get information about the requested product ID.
    - **pid**: BigInt Product ID
    """
    product = crud_product.get_product_by_id(db=db, product_id=pid)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {pid} not found."
        )
    return product


@router.post(
    "/add",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new product",
    description="Creates a new product in the database with validated fields."
)
def add_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Add a new product to the database.
    - **name**: Product name (max 100 characters)
    - **category**: enum ('finished', 'semi-finished', 'raw')
    - **description**: Product description (max 250 characters)
    - **product_image**: Image URL
    - **sku**: Stock Keeping Unit (max 100 characters)
    - **unit_of_measure**: enum ('mtr', 'mm', 'ltr', 'ml', 'cm', 'mg', 'gm', 'unit', 'pack')
    - **lead_time**: Lead time in days
    """
    return crud_product.create_product(db=db, product_in=product_in)


@router.put(
    "/{pid}/update",
    response_model=ProductResponse,
    summary="Update an existing product",
    description="Updates an existing product by product ID."
)
@router.patch(
    "/{pid}/update",
    response_model=ProductResponse,
    summary="Update an existing product (PATCH)",
    description="Partially updates an existing product by product ID.",
    include_in_schema=False
)
def update_product(
    product_in: ProductUpdate,
    pid: int = Path(..., ge=1, description="Unique Product ID"),
    db: Session = Depends(get_db)
):
    """
    Updates existing product with product ID in the database.
    - **pid**: Product ID to update
    - Optional fields to update: name, category, description, product_image, sku, unit_of_measure, lead_time
    """
    db_product = crud_product.get_product_by_id(db=db, product_id=pid)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {pid} not found."
        )

    updated_product = crud_product.update_product(
        db=db, db_product=db_product, product_in=product_in
    )
    return updated_product
