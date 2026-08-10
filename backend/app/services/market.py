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
    def parse_contact_info_to_json(contact_str: str) -> list:
        """将 Excel 中的联系电话字符串解析为符合规范的 JSON 列表"""
        if not contact_str or pd.isna(contact_str):
            return []

        # 使用正则表达式匹配逗号、分号、换行符、斜杠等分隔符
        phones = [p.strip() for p in re.split(r'[,，;；\n/]+', str(contact_str)) if p.strip()]

        contact_list = []
        for phone in phones:
            contact_list.append({
                "name": "待查询",
                "phone": phone,
                "is_sms_sent": False
            })
        return contact_list

    @staticmethod
    def parse_email_to_json(email_str: str) -> list:
        """将 Excel 中的邮箱字符串解析为符合规范的 JSON 列表"""
        if not email_str or pd.isna(email_str):
            return []

        # 使用正则表达式匹配常见的邮箱分隔符
        emails = [e.strip() for e in re.split(r'[,，;；\n/]+', str(email_str)) if e.strip()]

        email_list = []
        for email in emails:
            email_list.append({
                "email": email,
                "is_sent": False
            })
        return email_list

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

                # 转换联系方式与邮箱为 JSON 结构
                contact_json = MarketService.parse_contact_info_to_json(row.get('contact_info'))
                email_json = MarketService.parse_email_to_json(row.get('email'))

                # 处理分类默认值（防止 Excel 中出现空值或类型不对）
                category_val = row.get('enterprise_category')
                try:
                    category_int = int(category_val) if not pd.isna(category_val) else 5
                except (ValueError, TypeError):
                    category_int = 5

                new_ent = MarketEnterprise(
                    region=str(row.get('region', '')) if not pd.isna(row.get('region')) else '',
                    enterprise_name=ent_name,
                    legal_representative=str(row.get('legal_representative', '')) if not pd.isna(
                        row.get('legal_representative')) else '',
                    contact_info=contact_json,  # 存储 JSON 列表
                    email=email_json,  # 存储 JSON 列表
                    establishment_date=str(row.get('establishment_date', '')) if not pd.isna(
                        row.get('establishment_date')) else '',
                    registered_capital=capital_num,
                    enterprise_type=str(row.get('enterprise_type', '')) if not pd.isna(
                        row.get('enterprise_type')) else '',
                    registered_address=str(row.get('registered_address', '')) if not pd.isna(
                        row.get('registered_address')) else '',
                    enterprise_category=category_int,
                    is_intention=False,  # 默认不是意向客户
                    is_signed=False  # 默认未签约
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
