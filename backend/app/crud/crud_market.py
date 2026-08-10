from sqlalchemy.orm import Session
from sqlalchemy import cast, String
from typing import Optional, List, Dict, Any
from app.models.market import MarketEnterprise
from app.schemas.market import MarketEnterpriseCreate, MarketEnterpriseUpdate


class MarketCRUD:
    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(MarketEnterprise).filter(MarketEnterprise.enterprise_name == name).first()

    @staticmethod
    def get_list_with_page(
            db: Session,
            region: Optional[str] = None,
            enterprise_name: Optional[str] = None,
            legal_representative: Optional[str] = None,
            contact_info: Optional[str] = None,
            email: Optional[str] = None,
            enterprise_category: Optional[int] = None,
            is_intention: Optional[bool] = None,  # 🆕 新增：意向客户筛选
            is_signed: Optional[bool] = None,  # 🆕 新增：签约客户筛选
            sort_field: Optional[str] = None,  # 'registered_capital' 或 'establishment_date'
            sort_order: Optional[str] = 'asc',  # 'asc' 或 'desc' 从第一个开始显示
            page: int = 1,
            page_size: int = 10
    ):
        query = db.query(MarketEnterprise)

        # 1. 基础文本字段模糊查询
        if region:
            query = query.filter(MarketEnterprise.region.like(f"%{region}%"))
        if enterprise_name:
            query = query.filter(MarketEnterprise.enterprise_name.like(f"%{enterprise_name}%"))
        if legal_representative:
            query = query.filter(MarketEnterprise.legal_representative.like(f"%{legal_representative}%"))

        # 2. JSON 字段模糊检索（转为 String 后检索，可匹配 phone/name/email 各种子字段）
        if contact_info:
            query = query.filter(cast(MarketEnterprise.contact_info, String).like(f"%{contact_info}%"))
        if email:
            query = query.filter(cast(MarketEnterprise.email, String).like(f"%{email}%"))

        # 3. 类别过滤
        if enterprise_category:
            query = query.filter(MarketEnterprise.enterprise_category == enterprise_category)

        # 4. 🆕 布尔精准筛选 (意向/签约)
        if is_intention is not None:
            query = query.filter(MarketEnterprise.is_intention == is_intention)
        if is_signed is not None:
            query = query.filter(MarketEnterprise.is_signed == is_signed)

        # 获取符合条件的总数
        total = query.count()

        # 5. 动态排序处理
        if sort_field == "registered_capital":
            col = MarketEnterprise.registered_capital
            query = query.order_by(col.desc() if sort_order == "desc" else col.asc())
        elif sort_field == "establishment_date":
            col = MarketEnterprise.establishment_date
            query = query.order_by(col.desc() if sort_order == "desc" else col.asc())
        else:
            query = query.order_by(MarketEnterprise.id.asc())

        # 6. 分页切片
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return total, items

    # ==========================================
    # 🆕 额外补充常用的增删改基础 CRUD 方法
    # ==========================================

    @staticmethod
    def create(db: Session, obj_in: MarketEnterpriseCreate) -> MarketEnterprise:
        """创建企业信息"""
        # 将 Pydantic 对象转为字典（支持 JSON 嵌套字段序列化）
        db_obj = MarketEnterprise(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, db_obj: MarketEnterprise, obj_in: MarketEnterpriseUpdate) -> MarketEnterprise:
        """更新企业信息"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, enterprise_id: int) -> bool:
        """删除单个企业信息"""
        db_obj = db.query(MarketEnterprise).filter(MarketEnterprise.id == enterprise_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False
