from fastapi import APIRouter, UploadFile, File
import uuid

from user_app.utils.oss import bucket
from user_app.config import OSS_BUCKET, OSS_ENDPOINT

router = APIRouter()


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    # 生成唯一文件名
    filename = f"{uuid.uuid4()}_{file.filename}"

    # 读取文件内容
    content = await file.read()

    # 上传到 OSS
    bucket.put_object(filename, content)

    # 拼接图片 URL
    url = f"https://{OSS_BUCKET}.{OSS_ENDPOINT}/{filename}"

    return {
        "filename": filename,
        "url": url
    }