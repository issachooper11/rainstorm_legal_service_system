from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MarketEnterpriseResponse(BaseModel):
    id: int
    region: Optional[str] = None
    enterprise_name: str
    legal_representative: Optional[str] = None
    contact_info: Optional[str] = None
    email: Optional[str] = None
    establishment_date: Optional[str] = None
    registered_capital: Optional[float] = 0.0
    enterprise_type: Optional[str] = None
    registered_address: Optional[str] = None
    enterprise_category: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MarketPageResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[MarketEnterpriseResponse]
