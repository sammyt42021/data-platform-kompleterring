from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    """Basic product shape used after cleaning."""

    product_id: int = Field(gt=0)
    product_name: str = Field(min_length=2)
    category: str = Field(min_length=2)
    brand: str = Field(min_length=2)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class TopProductEvent(BaseModel):
    """Kafka event for one of the top expensive products."""

    event_type: Literal["top_expensive_product"] = "top_expensive_product"
    event_id: str
    emitted_at: datetime
    payload: ProductSchema
