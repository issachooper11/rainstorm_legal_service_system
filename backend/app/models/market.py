from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class MarketEnterprise(Base):
    __tablename__ = "market_enterprises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(100), index=True, comment="地区")
    enterprise_name = Column(String(255), unique=True, index=True, comment="企业名称")
    legal_representative = Column(String(100), comment="法定代表人")
    contact_info = Column(Text, comment="联系方式")
    email = Column(Text, comment="邮箱")
    establishment_date = Column(String(50), comment="成立日期")

    # 纯数字注册资本，用于精确排序
    registered_capital = Column(Float, default=0.0, index=True, comment="注册资本(万元)")

    enterprise_type = Column(String(100), comment="企业(机构)类型")
    registered_address = Column(String(255), comment="注册地址")
    enterprise_category = Column(Integer, default=5, index=True, comment="企业类别(1-5)")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    # 加上这行，与 EnterpriseTrace 模型中的 back_populates 对应
    traces = relationship("EnterpriseTrace", back_populates="enterprise", cascade="all, delete-orphan")
