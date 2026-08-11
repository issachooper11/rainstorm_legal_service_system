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

        # 2. 组装 HTML 正文内容（将前端传入的 \n 转换为 <br>）
        formatted_body = req.body.replace('\n', '<br>')

        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #f4f5f7; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
  <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f4f5f7; padding: 25px 0;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; border: 1px solid #eaedf1; overflow: hidden;">

          <!-- 顶部品牌 Header -->
          <tr>
            <td style="background-color: #1a2b4c; padding: 18px 25px;">
              <span style="color: #ffffff; font-size: 16px; font-weight: bold; letter-spacing: 1px;">北京觅理律师事务所</span>
              <span style="color: #a0aec0; font-size: 12px; float: right; margin-top: 3px;">常年法律顾问团队</span>
            </td>
          </tr>

          <!-- 正文主体 -->
          <tr>
            <td style="padding: 30px 25px;">

              <!-- 1. 动态格式化后的正文内容 -->
              <div style="font-size: 14px; color: #2c3e50; line-height: 1.8; word-break: break-word;">
                {formatted_body}
              </div>

              <!-- 2. 营销 CTA 引导按钮 -->
              <div style="text-align: center; margin: 28px 0 20px 0;">
                <a href="mailto:{settings.SMTP_USER}?subject=预约免费法律体检评估" 
                   style="background-color: #1a2b4c; color: #ffffff; padding: 12px 28px; text-decoration: none; font-size: 14px; font-weight: bold; border-radius: 4px; display: inline-block;">
                   👉 点击直接回复邮件，预约 15 分钟免费解读
                </a>
              </div>

              <!-- 分割线 -->
              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="margin: 25px 0 20px 0;">
                <tr>
                  <td style="border-top: 1px solid #eef2f7;"></td>
                </tr>
              </table>

              <!-- 3. 随信海报大图展示区 -->
              <div style="text-align: center; margin-bottom: 20px;">
                <p style="font-size: 13px; color: #1a2b4c; margin: 0 0 12px 0; font-weight: bold;">
                  ▼ 随信附带《企业法律健康体检清单》
                </p>
                <img src="cid:poster_img_cid" alt="企业法律健康体检清单" width="550" style="width: 100%; max-width: 550px; height: auto; border-radius: 6px; display: block; margin: 0 auto; border: 1px solid #e2e8f0;" />
              </div>

              <!-- 4. 二维码横向卡片 -->
              <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px; margin-top: 15px;">
                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <!-- 左侧：二维码图片 -->
                    <td width="110" valign="middle" style="text-align: center;">
                      <img src="cid:qrcode_img_cid" alt="微信二维码" width="95" height="95" style="width: 95px; height: 95px; border-radius: 6px; border: 1px solid #cbd5e1; display: block;" />
                    </td>
                    <!-- 右侧：扫码引导文案 -->
                    <td valign="middle" style="padding-left: 18px;">
                      <p style="font-size: 15px; font-weight: bold; color: #0f172a; margin: 0 0 6px 0;">
                        扫码添加并发送公司名称，即可免费获取《企业合规清单》、预约线上评估。
                      </p>
                    </td>
                  </tr>
                </table>
              </div>

            </td>
          </tr>

          <!-- 页脚 Footer -->
          <tr>
            <td style="background-color: #fafbfc; padding: 15px 25px; text-align: center; border-top: 1px solid #f0f0f0;">
              <p style="font-size: 12px; color: #a0aec0; margin: 0; line-height: 1.5;">
                助力企业合规稳健生长<br>
                如需退订，请回复“退订”
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
        """

        # 挂载 HTML 文本
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        # 3. 分别挂载海报图片和二维码图片
        poster_path = settings.CHECKLIST_POSTER_PATH
        qrcode_path = settings.PRODUCT_SCAN_PATH

        # 3.1 挂载海报 (poster_img_cid)
        if poster_path.is_file():
            with open(poster_path, 'rb') as f:
                img_poster = MIMEImage(f.read())
                img_poster.add_header('Content-ID', '<poster_img_cid>')
                img_poster.add_header(
                    'Content-Disposition',
                    'inline',
                    filename=('utf-8', '', poster_path.name)
                )
                msg.attach(img_poster)
            print(f"✅ 成功挂载海报图片: {poster_path.name}")
        else:
            print(f"⚠️ [警告] 海报文件未找到: {poster_path.resolve()}")

        # 3.2 挂载二维码 (qrcode_img_cid)
        if qrcode_path.is_file():
            with open(qrcode_path, 'rb') as f:
                img_qrcode = MIMEImage(f.read())
                img_qrcode.add_header('Content-ID', '<qrcode_img_cid>')
                img_qrcode.add_header(
                    'Content-Disposition',
                    'inline',
                    filename=('utf-8', '', qrcode_path.name)
                )
                msg.attach(img_qrcode)
            print(f"✅ 成功挂载二维码图片: {qrcode_path.name}")
        else:
            print(f"⚠️ [警告] 二维码文件未找到: {qrcode_path.resolve()}")

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
