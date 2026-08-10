from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class MarketEnterprise(Base):
    __tablename__ = "market_enterprises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(100), index=True, comment="地区")
    enterprise_name = Column(String(255), unique=True, index=True, comment="企业名称")
    legal_representative = Column(String(100), comment="法定代表人")

    # 更改为 JSON 类型，存储嵌套列表数据
    # contact_info 格式：[{"name": "待查询", "phone": "136...", "is_sms_sent": false}]
    contact_info = Column(JSON, default=list, comment="联系方式列表(JSON)")

    # email 格式：[{"email": "xxx@qq.com", "is_sent": false}]
    email = Column(JSON, default=list, comment="邮箱列表(JSON)")

    establishment_date = Column(String(50), comment="成立日期")

    # 纯数字注册资本，用于精确排序
    registered_capital = Column(Float, default=0.0, index=True, comment="注册资本(万元)")

    enterprise_type = Column(String(100), comment="企业(机构)类型")
    registered_address = Column(String(255), comment="注册地址")
    enterprise_category = Column(Integer, default=5, index=True, comment="企业类别(1-5)")

    # 新增字段：意向与签约状态
    is_intention = Column(Boolean, default=False, index=True, comment="是否为意向客户")
    is_signed = Column(Boolean, default=False, index=True, comment="是否签约")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 与 EnterpriseTrace 模型对应
    traces = relationship("EnterpriseTrace", back_populates="enterprise", cascade="all, delete-orphan")
