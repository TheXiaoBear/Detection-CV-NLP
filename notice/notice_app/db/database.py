import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from infra.nacos.settings import settings
# 先找环境变量，没有就用默认值
# DATABASE_URL = os.getenv(
#     "DATABASE_URL", # 先从系统的环境变量里找这个钥匙
#     "mysql+pymysql://root:123456@localhost:3306/target" # 找不到就用这个默认备用钥匙
# )

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{settings.MYSQL_USER}:"
    f"{settings.MYSQL_PASSWORD}@"
    f"{settings.MYSQL_HOST}:"
    f"{settings.MYSQL_PORT}/"
    f"{settings.MYSQL_DB}"
)

engine = create_engine(
    DATABASE_URL,       # 上面拼好的连接地址
    pool_pre_ping=True, # 使用前" ping "一下，确认连接还活着
    pool_recycle=3600,  # 连接出生 1 小时后强制退休，换新的
    pool_size=10,       # 常备 10 条连接（长工）
    max_overflow=20,    # 忙不过来时最多再招 20 条临时工（总共最多 30 条）
)

# Session 是一个工作单元，通过这个单元将对数据库的操作提交给数据库
SessionLocal = sessionmaker(
    autocommit=False,   # 不自动提交（显式控制事务）
    autoflush=False,    # 不自动刷新（显式控制何时发 SQL）
    bind=engine         # 绑到上面建好的总阀门上
)

# Base 是一个"自动登记簿 + 图纸母版"。
# 所有继承它的模型类，会被自动记录到一本花名册（metadata）里，方便以后统一建表、统一查表。
Base = declarative_base()


# 统一依赖（推荐集中放这里）
def get_db():
    db = SessionLocal() # 从工厂里叫出一个业务员（创建一个 Session）
    try:
        # 交给 FastAPI 的路由函数，表示"数据库连接给你，去查数据吧"
        yield db # ← 把业务员交给路由函数使用
    finally:
        db.close() # 不管路由函数成功还是报错，用完必须关门