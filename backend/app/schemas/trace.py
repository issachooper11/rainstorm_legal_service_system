from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# 创建跟进记录的请求入参（不需要传 creator，由后端从登录态获取）
class EnterpriseTraceCreate(BaseModel):
    trace_type: int = Field(..., ge=1, le=4, description="跟进方式: 1-邮件, 2-电话, 3-微信, 4-线下")
    content: str = Field(..., min_length=1, description="跟进详细内容")


# 返回给前端的跟进记录详情
class EnterpriseTraceResponse(BaseModel):
    id: int
    enterprise_id: int
    trace_type: int
    content: str
    creator_id: int
    creator_name: str
    created_at: datetime

    class Config:
        from_attributes = True
