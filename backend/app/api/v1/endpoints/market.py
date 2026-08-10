import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from fastapi import APIRouter, Depends, File, UploadFile, Query, HTTPException, status
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy.orm import Session
from typing import Optional

from app.core.config import settings
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


# 定义请求 Body 数据结构
class SendEmailReq(BaseModel):
    enterprise_id: int
    email: EmailStr
    subject: str
    body: str
    # 允许忽略前端传入的多余字段（忽略 extra 属性）
    model_config = ConfigDict(extra='ignore')


@router.post("/email/send")
def send_marketing_email(req: SendEmailReq):
    """
    发送营销邮件接口
    """
    if not settings.SMTP_USER or not settings.SMTP_PASS:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="邮件服务未配置，请检查 .env 中的 SMTP_USER 与 SMTP_PASS"
        )

    try:
        # 1. 创建 related 类型的邮件主体（用于正文内嵌图片）
        msg = MIMEMultipart('related')

        # 解决发件人防诈骗警告：formataddr 会自动对发件人中文名进行 RFC 2047 编码
        msg['From'] = formataddr((settings.SENDER_NAME, settings.SMTP_USER))
        msg['To'] = req.email
        msg['Subject'] = req.subject  # Python email 模块会自动处理 Header 编码

        # 2. 组装 HTML 正文
        formatted_body = req.body.replace('\n', '<br>')
        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>邮件正文</title>
        </head>
        <body style="margin: 0; padding: 0; background-color: #f4f5f7; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; -webkit-font-smoothing: antialiased;">
          <!-- 最外层卡片容器 (使用 table 保证所有邮件客户端居中) -->
          <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f4f5f7; padding: 20px 0;">
            <tr>
              <td align="center">
                <!-- 正文主卡片 -->
                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; border: 1px solid #eaedf1; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                  <tr>
                    <td style="padding: 30px 25px;">
                      
                      <!-- 邮件主要文案内容 -->
                      <div style="font-size: 15px; color: #2c3e50; line-height: 1.7; word-break: break-word;">
                        {formatted_body}
                      </div>

                      <!-- 分割线 -->
                      <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="margin: 25px 0 20px 0;">
                        <tr>
                          <td style="border-top: 1px solid #eef2f7;"></td>
                        </tr>
                      </table>

                      <!-- 海报图片展示区 -->
                      <div style="text-align: center;">
                        <p style="font-size: 12px; color: #909399; margin: 0 0 12px 0; font-weight: normal;">
                          --- 随信附带《企业法律健康体检清单》---
                        </p>
                        <img src="cid:poster_img_cid" alt="企业法律健康体检清单" width="550" style="width: 100%; max-width: 550px; height: auto; border-radius: 6px; display: block; margin: 0 auto; border: 0;" />
                      </div>

                    </td>
                  </tr>
                </table>
                <!-- 卡片结束 -->
                
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

        # 直接挂载 HTML 文本内容
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        # 3. 挂载海报图片（使用 config.py 定义的 Path 对象）
        poster_path = settings.CHECKLIST_POSTER_PATH

        if poster_path.is_file():
            with open(poster_path, 'rb') as f:
                img = MIMEImage(f.read())
                # 指定 Content-ID 供 HTML 中的 <img src="cid:poster_img_cid"> 引用
                img.add_header('Content-ID', '<poster_img_cid>')
                # 兼容中文名的附件头配置
                img.add_header(
                    'Content-Disposition',
                    'inline',
                    filename=('utf-8', '', poster_path.name)
                )
                msg.attach(img)
            print(f"✅ 成功加载并挂载海报图片: {poster_path.name}")
        else:
            print(f"⚠️ [警告] 海报图片未找到，预计路径: {poster_path.resolve()}")

        # 4. 发送邮件
        with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.sendmail(settings.SMTP_USER, [req.email], msg.as_string())

        return {"code": 200, "message": "邮件发送成功"}

    except Exception as e:
        print(f"❌ 发送邮件报错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"邮件发送失败: {str(e)}"
        )


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
