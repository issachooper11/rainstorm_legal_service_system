from fastapi import APIRouter, Depends, File, UploadFile, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models.market import MarketEnterprise
from app.services.market import MarketService
from app.crud.crud_market import MarketCRUD
from app.schemas.market import (
    MarketPageResponse,
    MarketEnterpriseResponse,
    MarketEnterpriseUpdate
)

router = APIRouter(prefix="/market", tags=["市场信息管理"])


@router.post("/import")
def import_market(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Excel 批量导入市场企业数据"""
    result = MarketService.import_excel_service(file, db)
    return {
        "code": 200,
        "message": f"导入完成！成功新增 {result['success_count']} 条数据。",
        "data": result
    }


@router.get("/list", response_model=MarketPageResponse)
def get_market_list(
        region: Optional[str] = Query(None, description="地区筛选"),
        enterprise_name: Optional[str] = Query(None, description="企业名称筛选"),
        legal_representative: Optional[str] = Query(None, description="法定代表人筛选"),
        contact_info: Optional[str] = Query(None, description="联系方式筛选"),
        email: Optional[str] = Query(None, description="邮箱筛选"),
        enterprise_category: Optional[int] = Query(None, description="企业类别 1-5"),
        is_intention: Optional[bool] = Query(None, description="是否意向客户筛选"),
        is_signed: Optional[bool] = Query(None, description="是否签约筛选"),
        sort_field: Optional[str] = Query(None, description="排序字段: registered_capital 或 establishment_date"),
        sort_order: Optional[str] = Query("asc", description="排序规则: asc 或 desc"),
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, description="每页条数"),
        db: Session = Depends(get_db)
):
    """分页与多条件检索市场企业列表"""
    if page_size not in [5, 10, 25, 50]:
        page_size = 10  # 默认兜底

    total, items = MarketCRUD.get_list_with_page(
        db=db,
        region=region,
        enterprise_name=enterprise_name,
        legal_representative=legal_representative,
        contact_info=contact_info,
        email=email,
        enterprise_category=enterprise_category,
        is_intention=is_intention,
        is_signed=is_signed,
        sort_field=sort_field,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }


@router.put("/{enterprise_id}", response_model=MarketEnterpriseResponse)
def update_market_enterprise(
        enterprise_id: int,
        obj_in: MarketEnterpriseUpdate,
        db: Session = Depends(get_db)
):
    """更新企业信息（支持修改联系人/邮箱 JSON 列表、意向状态、签约状态等）"""
    db_obj = db.query(MarketEnterprise).filter(MarketEnterprise.id == enterprise_id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="未找到对应的企业信息")

    updated_obj = MarketCRUD.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return updated_obj


@router.delete("/{enterprise_id}")
def delete_market_enterprise(
        enterprise_id: int,
        db: Session = Depends(get_db)
):
    """删除单条企业记录"""
    success = MarketCRUD.delete(db=db, enterprise_id=enterprise_id)
    if not success:
        raise HTTPException(status_code=404, detail="未找到对应的企业信息或已删除")
    return {"code": 200, "message": "删除成功"}
