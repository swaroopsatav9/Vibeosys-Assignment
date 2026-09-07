from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from app.models.product import ProductCategory, UnitOfMeasure


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product name (max 100 characters)",
        examples=["Industrial Electric Motor"]
    )
    category: ProductCategory = Field(
        ...,
        description="Product category: finished, semi-finished, or raw",
        examples=["finished"]
    )
    description: Optional[str] = Field(
        None,
        max_length=250,
        description="Product description (max 250 characters)",
        examples=["High-torque 3-phase AC induction motor"]
    )
    product_image: Optional[str] = Field(
        None,
        description="Product image URL",
        examples=["https://example.com/images/motor.jpg"]
    )
    sku: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Stock Keeping Unit (max 100 characters)",
        examples=["MOT-IND-001"]
    )
    unit_of_measure: UnitOfMeasure = Field(
        ...,
        description="Unit of measure: mtr, mm, ltr, ml, cm, mg, gm, unit, pack",
        examples=["unit"]
    )
    lead_time: int = Field(
        ...,
        ge=0,
        le=999,
        description="Lead time in days (0-999)",
        examples=[14]
    )


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Product name (max 100 characters)"
    )
    category: Optional[ProductCategory] = Field(
        None,
        description="Product category: finished, semi-finished, or raw"
    )
    description: Optional[str] = Field(
        None,
        max_length=250,
        description="Product description (max 250 characters)"
    )
    product_image: Optional[str] = Field(
        None,
        description="Product image URL"
    )
    sku: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Stock Keeping Unit (max 100 characters)"
    )
    unit_of_measure: Optional[UnitOfMeasure] = Field(
        None,
        description="Unit of measure: mtr, mm, ltr, ml, cm, mg, gm, unit, pack"
    )
    lead_time: Optional[int] = Field(
        None,
        ge=0,
        le=999,
        description="Lead time in days (0-999)"
    )


class ProductResponse(ProductBase):
    id: int = Field(..., description="Unique product ID", examples=[1])
    created_date: datetime = Field(..., description="Timestamp when the product was created")
    updated_date: datetime = Field(..., description="Timestamp when the product was last updated")

    model_config = ConfigDict(from_attributes=True)


class ProductPaginationResponse(BaseModel):
    items: List[ProductResponse] = Field(..., description="List of products on current page")
    total_records: int = Field(..., description="Total number of products in database", examples=[45])
    current_page: int = Field(..., description="Current page number", examples=[1])
    page_size: int = Field(..., description="Number of records per page (default: 10)", examples=[10])
    total_pages: int = Field(..., description="Total number of pages", examples=[5])
    has_next: bool = Field(..., description="Whether there is a next page", examples=[True])
    has_previous: bool = Field(..., description="Whether there is a previous page", examples=[False])


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None
