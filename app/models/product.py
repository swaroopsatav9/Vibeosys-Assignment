import enum
from sqlalchemy import Column, BigInteger, String, Integer, Text, DateTime, Enum as SAEnum, func
from app.database import Base


class ProductCategory(str, enum.Enum):
    FINISHED = "finished"
    SEMI_FINISHED = "semi-finished"
    RAW = "raw"


class UnitOfMeasure(str, enum.Enum):
    MTR = "mtr"
    MM = "mm"
    LTR = "ltr"
    ML = "ml"
    CM = "cm"
    MG = "mg"
    GM = "gm"
    UNIT = "unit"
    PACK = "pack"


class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(
        SAEnum(ProductCategory, values_callable=lambda obj: [e.value for e in obj], name="product_category_enum"),
        nullable=False
    )
    description = Column(String(250), nullable=True)
    product_image = Column(Text, nullable=True)  # varchar(max) image URL
    sku = Column(String(100), nullable=False, index=True)
    unit_of_measure = Column(
        SAEnum(UnitOfMeasure, values_callable=lambda obj: [e.value for e in obj], name="product_uom_enum"),
        nullable=False
    )
    lead_time = Column(Integer, nullable=False)  # lead time in days
    created_date = Column(DateTime, server_default=func.now(), nullable=False)
    updated_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
