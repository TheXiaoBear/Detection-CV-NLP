from datetime import datetime, timedelta, UTC # 时间处理
from jose import jwt, JWTError # JWT 库：造票 + 验票
import os

JWT_SECRET = os.getenv(
    "JWT_SECRET", # 先从系统的环境变量里找这个钥匙
    "123456" # 找不到就用这个默认备用钥匙
)

SECRET_KEY = JWT_SECRET # 签名密钥：防伪钢印
ALGORITHM = "HS256" # 签名算法：HS256（HMAC-SHA256）
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 票的有效期：60分钟


def create_access_token(data: dict):
    # 复制传入数据，避免修改原始字典
    to_encode = data.copy()

    # 计算过期时间：现在 + 60分钟
    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # 把过期时间塞进待编码的数据里
    to_encode.update({"exp": expire})

    # 签名打包，生成 JWT 字符串
    return jwt.encode(
        to_encode,  # 载荷（Payload）：你要传递的数据
        SECRET_KEY,  # 密钥：用于签名防伪
        algorithm=ALGORITHM  # 算法：签名方式
    )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,                # 客户端带来的票
            SECRET_KEY,           # 用同样的密钥验签
            algorithms=[ALGORITHM] # 指定允许的算法（安全需要）
        )
        return payload              # 验票通过，返回原始数据
    except JWTError:
        return None                 # 验票失败（伪造/过期/篡改），静默返回 None