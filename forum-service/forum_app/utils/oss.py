import oss2
import uuid
from user_app.config import (
    OSS_ACCESS_KEY_ID,
    OSS_ACCESS_KEY_SECRET,
    OSS_BUCKET,
    OSS_ENDPOINT
)

# 创建认证对象
auth = oss2.Auth(
    OSS_ACCESS_KEY_ID,
    OSS_ACCESS_KEY_SECRET
)

# 创建 Bucket 对象
bucket = oss2.Bucket(
    auth,
    OSS_ENDPOINT,
    OSS_BUCKET
)


def upload_file(file_bytes: bytes, filename: str):

    # 防止重名
    object_name = f"{uuid.uuid4()}_{filename}"

    # 上传
    bucket.put_object(object_name, file_bytes)

    # 返回访问 URL
    url = (
        f"https://{OSS_BUCKET}.{OSS_ENDPOINT}/{object_name}"
    )

    return url