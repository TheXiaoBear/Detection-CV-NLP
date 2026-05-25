from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from io import BytesIO  # ← 把内存 bytes 包装成"文件对象"
from PIL import Image  # ← Python 图片处理标准库

from utils.oss import bucket
from config import OSS_BUCKET, OSS_ENDPOINT

router = APIRouter()

# ========== 可配置的限制 ==========
MAX_WIDTH = 4096  # 最大宽度
MAX_HEIGHT = 4096  # 顺便也限制下高度
MAX_FILE_SIZE_MB = 10  # 可选：顺便限制文件大小（MB）


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # -----------------------
    # 1. 读取文件到内存
    # -----------------------
    content = await file.read()

    # 可选：先限制文件体积（防止有人传 1GB 的"图片"把内存撑爆）
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"文件过大，最大允许 {MAX_FILE_SIZE_MB}MB"
        )

    # -----------------------
    # 2. 解析图片，获取宽高
    # -----------------------
    try:
        # BytesIO 的作用：把内存里的 bytes 包装成一个"可读的文件对象"
        # 这样 Pillow 就能像打开本地文件一样打开它
        image = Image.open(BytesIO(content))
        width, height = image.size
    except Exception:
        # 如果用户上传的是 .txt、.exe 等非图片文件，Pillow 会报错
        raise HTTPException(
            status_code=400,
            detail="无法识别图片格式，请上传有效的图片文件"
        )

    # -----------------------
    # 3. 尺寸限制检查
    # -----------------------
    if width > MAX_WIDTH:
        raise HTTPException(
            status_code=400,
            detail=f"图片宽度 {width}px 超过限制（最大 {MAX_WIDTH}px）"
        )

    if height > MAX_HEIGHT:
        raise HTTPException(
            status_code=400,
            detail=f"图片高度 {height}px 超过限制（最大 {MAX_HEIGHT}px）"
        )

    # -----------------------
    # 4. 上传 OSS（和原来一样）
    # -----------------------
    filename = f"{uuid.uuid4()}_{file.filename}"
    bucket.put_object(filename, content)

    url = f"https://{OSS_BUCKET}.{OSS_ENDPOINT}/{filename}"

    # -----------------------
    # 5. 返回（顺便把尺寸告诉前端，方便调试）
    # -----------------------
    return {
        "filename": filename,
        "url": url,
        "width": width,
        "height": height
    }