from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class EnterpriseTrace(Base):
    __tablename__ = "enterprise_traces"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    enterprise_id = Column(Integer, ForeignKey("market_enterprises.id", ondelete="CASCADE"), nullable=False,
                           comment="关联的企业ID")

    trace_type = Column(Integer, nullable=False, comment="跟进方式: 1-邮件, 2-电话, 3-微信, 4-线下")
    content = Column(Text, nullable=False, comment="跟进详细内容")

    # 记录创建人信息（基于登录用户自动绑定）
    creator_id = Column(Integer, nullable=False, comment="跟进人ID")
    creator_name = Column(String(50), nullable=False, comment="跟进人姓名")

    created_at = Column(DateTime, default=datetime.now, comment="跟进时间")

    # 关联企业主表
    enterprise = relationship("MarketEnterprise", back_populates="traces")
