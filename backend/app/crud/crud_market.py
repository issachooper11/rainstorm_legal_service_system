from sqlalchemy.orm import Session
from typing import Optional
from app.models.market import MarketEnterprise


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
            sort_field: Optional[str] = None,  # 'registered_capital' 或 'establishment_date'
            sort_order: Optional[str] = 'asc',  # 'asc' 或 'desc'
            page: int = 1,
            page_size: int = 10
    ):
        query = db.query(MarketEnterprise)

        # 多条件模糊查询
        if region:
            query = query.filter(MarketEnterprise.region.like(f"%{region}%"))
        if enterprise_name:
            query = query.filter(MarketEnterprise.enterprise_name.like(f"%{enterprise_name}%"))
        if legal_representative:
            query = query.filter(MarketEnterprise.legal_representative.like(f"%{legal_representative}%"))
        if contact_info:
            query = query.filter(MarketEnterprise.contact_info.like(f"%{contact_info}%"))
        if email:
            query = query.filter(MarketEnterprise.email.like(f"%{email}%"))
        if enterprise_category:
            query = query.filter(MarketEnterprise.enterprise_category == enterprise_category)

        total = query.count()

        # 排序处理
        if sort_field == "registered_capital":
            col = MarketEnterprise.registered_capital
            query = query.order_by(col.desc() if sort_order == "desc" else col.asc())
        elif sort_field == "establishment_date":
            col = MarketEnterprise.establishment_date
            query = query.order_by(col.desc() if sort_order == "desc" else col.asc())
        else:
            query = query.order_by(MarketEnterprise.id.desc())

        # 分页
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return total, items
