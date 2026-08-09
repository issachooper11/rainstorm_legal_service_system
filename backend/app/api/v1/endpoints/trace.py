from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db

from app.api.deps import get_current_user
from app.models.trace import EnterpriseTrace
from app.schemas.trace import EnterpriseTraceCreate, EnterpriseTraceResponse

# 假设你项目中已有获取当前登录用户的依赖项
# from app.core.deps import get_current_user

router = APIRouter(prefix="/trace", tags=["市场企业跟进记录"])


@router.post("/{enterprise_id}/traces", response_model=EnterpriseTraceResponse)
def create_enterprise_trace(
        enterprise_id: int,
        trace_in: EnterpriseTraceCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)  # 注入当前登录用户
):
    """
    给指定企业添加一条跟进记录
    """
    # 1. 校验企业是否存在
    # enterprise = db.query(MarketEnterprise).filter(MarketEnterprise.id == enterprise_id).first()
    # if not enterprise:
    #     raise HTTPException(status_code=404, detail="企业不存在")

    # 2. 创建跟进记录，自动绑定登录用户信息
    new_trace = EnterpriseTrace(
        enterprise_id=enterprise_id,
        trace_type=trace_in.trace_type,
        content=trace_in.content,
        creator_id=current_user.id,  # 从登录态获取用户ID
        creator_name=current_user.username  # 从登录态获取用户姓名
    )

    db.add(new_trace)
    db.commit()
    db.refresh(new_trace)
    return new_trace


@router.get("/{enterprise_id}/traces", response_model=List[EnterpriseTraceResponse])
def get_enterprise_traces(
        enterprise_id: int,
        db: Session = Depends(get_db)
):
    """
    获取某企业的所有跟进记录（按时间倒序）
    """
    traces = db.query(EnterpriseTrace) \
        .filter(EnterpriseTrace.enterprise_id == enterprise_id) \
        .order_by(EnterpriseTrace.created_at.desc()) \
        .all()

    return traces
