from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ==========================================
# 1. 嵌套子项结构 (联系方式与邮箱)
# ==========================================

class ContactItem(BaseModel):
    name: str = Field(default="待查询", description="联系人姓名，默认待查询")
    phone: str = Field(..., description="电话号码")
    is_sms_sent: bool = Field(default=False, description="是否已发送短信")


class EmailItem(BaseModel):
    email: str = Field(..., description="邮箱地址")
    is_sent: bool = Field(default=False, description="是否已发送邮件")


# ==========================================
# 2. 基础模型 (共享属性)
# ==========================================

class MarketEnterpriseBase(BaseModel):
    region: Optional[str] = None
    enterprise_name: str
    legal_representative: Optional[str] = None
    contact_info: List[ContactItem] = Field(default_factory=list, description="联系方式列表")
    email: List[EmailItem] = Field(default_factory=list, description="邮箱列表")
    establishment_date: Optional[str] = None
    registered_capital: Optional[float] = 0.0
    enterprise_type: Optional[str] = None
    registered_address: Optional[str] = None
    enterprise_category: Optional[int] = 5
    is_intention: bool = Field(default=False, description="是否为意向客户")
    is_signed: bool = Field(default=False, description="是否签约")


# ==========================================
# 3. 创建与更新请求模型
# ==========================================

class MarketEnterpriseCreate(MarketEnterpriseBase):
    pass


class MarketEnterpriseUpdate(BaseModel):
    region: Optional[str] = None
    enterprise_name: Optional[str] = None
    legal_representative: Optional[str] = None
    contact_info: Optional[List[ContactItem]] = None
    email: Optional[List[EmailItem]] = None
    establishment_date: Optional[str] = None
    registered_capital: Optional[float] = None
    enterprise_type: Optional[str] = None
    registered_address: Optional[str] = None
    enterprise_category: Optional[int] = None
    is_intention: Optional[bool] = None
    is_signed: Optional[bool] = None


# ==========================================
# 4. 响应模型 (单条数据与分页数据)
# ==========================================

class MarketEnterpriseResponse(MarketEnterpriseBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Pydantic v2 写法 (如果是 v1，请改为 orm_mode = True)


class MarketPageResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[MarketEnterpriseResponse]
