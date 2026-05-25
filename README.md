api：接收请求  
schemas：定义数据  
services：处理逻辑  
repository：操作数据库  
models：定义表  
db：提供连接  
main：启动项目

id
task_id
label
confidence
caption
bbox_image_path
heatmap_path
created_at

## 二、数据库引擎 Engine：管道的"总阀门"

Python

复制

```python
engine = create_engine(
    DATABASE_URL,       # 上面拼好的连接地址
    pool_pre_ping=True, # 使用前" ping "一下，确认连接还活着
    pool_recycle=3600,  # 连接出生 1 小时后强制退休，换新的
    pool_size=10,       # 常备 10 条连接（长工）
    max_overflow=20,    # 忙不过来时最多再招 20 条临时工（总共最多 30 条）
)
```

### 什么是 Engine？

想象数据库是**水库**，你的 FastAPI 程序是**城市**。`engine` 就是**自来水总公司**：

- 它管理着一堆通向水库的管道（**连接池**）
- 谁要用水（查数据），不用自己挖沟铺管，直接从池子里拿一根现成的

### 连接池参数详解（重点）

表格





| 参数            | 值           | 通俗解释               | 实际作用                                                     |
| :-------------- | :----------- | :--------------------- | :----------------------------------------------------------- |
| `pool_pre_ping` | `True`       | **"使用前敲敲门"**     | 拿连接前先发一个轻量测试信号，如果连接已断（如数据库重启过），自动丢弃换新，避免程序报错 |
| `pool_recycle`  | `3600`（秒） | **"连接寿命 1 小时"**  | MySQL 默认 8 小时会踢掉空闲连接。设置 1 小时主动换新，防止半夜被数据库踢掉导致报错 |
| `pool_size`     | `10`         | **"常备长工 10 人"**   | 程序启动就预先开好 10 条连接，随时待命。适合常规并发量       |
| `max_overflow`  | `20`         | **"临时工上限 20 人"** | 当 10 个长工都在忙，临时再开最多 20 条应急。忙完即焚，不长期占用 |

> 连接池的核心思想：**复用**。开数据库连接是很重的操作（要握手、验证、分配资源），池化后避免了"每次请求都新建连接"的巨大开销。

## 三、会话工厂 SessionLocal：借管道的"工单系统"

Python

复制

```python
SessionLocal = sessionmaker(
    autocommit=False,   # 不自动提交（显式控制事务）
    autoflush=False,    # 不自动刷新（显式控制何时发 SQL）
    bind=engine         # 绑到上面建好的总阀门上
)
```

### 什么是 Session？

`Session`（会话）是 SQLAlchemy 的**工作单元**。你可以把它理解为：

> 一个**办事窗口业务员**。所有"查数据、改数据、删数据"的操作，都必须通过这个业务员提交给数据库。

`sessionmaker` 不是 Session 本身，而是**"批量生产业务员的工厂模板"**。每次需要时调用 `SessionLocal()` 就能生出一个新业务员。

### 两个 False 的含义（非常重要）

表格





| 参数               | 设为 `False` 的原因                                          |
| :----------------- | :----------------------------------------------------------- |
| `autocommit=False` | **手动控制事务边界**。你执行 `db.commit()` 才真正写入数据库，执行 `db.rollback()` 可以撤销。如果设为 `True`，每条 SQL 自动提交，一旦出错无法回滚，数据容易脏 |
| `autoflush=False`  | **手动控制刷新时机**。`flush` 是把内存中的改动翻译成 SQL 发给数据库（但还没真正提交）。设为 `False` 后，只有调用 `db.flush()` 或 `db.commit()` 时才发 SQL，避免在复杂逻辑中频繁与数据库通信 |

**一句话**：这两个 `False` 让你**完全掌控节奏**，而不是让 SQLAlchemy 在背后偷偷发 SQL。

------

## 四、声明基类 Base：所有数据表的"设计图纸母版"

Python

复制

```python
Base = declarative_base()
```

### 含义

`Base` 是一个**元类（模板之母）**。你在其他文件里写模型时：

Python

复制

```python
from db.database import Base


class User(Base):  # ← 继承 Base
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
```

`Base` 会默默记录所有继承它的类（`User`、`Task` 等）。之后你在 `main.py` 里看到的：

Python

复制

```python
Base.metadata.create_all(bind=engine)
```

就是命令 `Base`：**"把你登记过的所有图纸，全部在数据库里建成真实的表！"**

------

## 五、依赖注入 get_db：FastAPI 的"数据库快递员"

Python

复制

```python
# 统一依赖（推荐集中放这里）
def get_db():
    db = SessionLocal()   # 从工厂里叫出一个业务员（创建一个 Session）
    try:
        yield db          # ← 把业务员交给路由函数使用
    finally:
        db.close()        # 不管路由函数成功还是报错，用完必须关门
```

### 这是整个文件**与 FastAPI 衔接最关键**的部分。

status：

pending
processing
success
failed

                                                                                                                  
                                                                                                                
cv-service                                                                                                               
mq                                                                                                                       
nlp-service                                                                                                              
user-sevice                                                                                                              
                                                                                                     
