from pydantic import BaseModel, root_validator
from uuid import UUID
from typing import Optional, Any
from app.utils import uuid_to_datetime

class ProductSchema(BaseModel):
    asin : str
    title : str
    
class ProductScrapeEventSchema(BaseModel):
    uuid : UUID
    asin: str
    title: Optional[str]

class ProductListSchema(BaseModel):
    asin : str
    title : str
    price_str : Optional[str]
    
class ProductScrapeEventDetailSchema(BaseModel):
    asin : str
    title : Optional[str]
    price_str :Optional[str]
    created : Optional[Any] = None
    
    @root_validator(pre=True)
    def time_from_uuid(cls, values):
        values['created'] = uuid_to_datetime(values['uuid'].time)
        return values