import re
import pandas as pd
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from app.models.market import MarketEnterprise
from app.crud.crud_market import MarketCRUD


class MarketService:
    @staticmethod
    def parse_capital_to_num(capital_str) -> float:
        if not capital_str or pd.isna(capital_str):
            return 0.0
        cleaned = str(capital_str).replace(',', '').strip()
        if "xxxx" in cleaned or cleaned == "":
            return 0.0
        match = re.search(r'([\d.]+)', cleaned)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return 0.0
        return 0.0

    @staticmethod
    def import_excel_service(file: UploadFile, db: Session):
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="只支持上传 .xlsx 或 .xls 格式的 Excel 文件")

        try:
            df = pd.read_excel(file.file)

            df.rename(columns={
                '地区': 'region',
                '企业名称': 'enterprise_name',
                '法定代表人': 'legal_representative',
                '联系方式': 'contact_info',
                '邮箱': 'email',
                '成立日期': 'establishment_date',
                '注册资本': 'registered_capital',
                '企业(机构)类型': 'enterprise_type',
                '注册地址': 'registered_address',
                '企业类别': 'enterprise_category'
            }, inplace=True)

            success_count = 0
            skipped_count = 0
            skipped_names = []

            for _, row in df.iterrows():
                ent_name = str(row.get('enterprise_name', '')).strip()
                if not ent_name or pd.isna(ent_name):
                    continue

                    # 查重：数据库有相同企业名称则不添加并记录
                if MarketCRUD.get_by_name(db, ent_name):
                    skipped_count += 1
                    skipped_names.append(ent_name)
                    continue

                capital_num = MarketService.parse_capital_to_num(row.get('registered_capital'))

                new_ent = MarketEnterprise(
                    region=str(row.get('region', '')),
                    enterprise_name=ent_name,
                    legal_representative=str(row.get('legal_representative', '')),
                    contact_info=str(row.get('contact_info', '')),
                    email=str(row.get('email', '')),
                    establishment_date=str(row.get('establishment_date', '')),
                    registered_capital=capital_num,
                    enterprise_type=str(row.get('enterprise_type', '')),
                    registered_address=str(row.get('registered_address', '')),
                    enterprise_category=int(row.get('enterprise_category', 5))
                )
                db.add(new_ent)
                success_count += 1

            db.commit()
            return {
                "success_count": success_count,
                "skipped_count": skipped_count,
                "skipped_names": skipped_names
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"解析或导入 Excel 异常: {str(e)}")
