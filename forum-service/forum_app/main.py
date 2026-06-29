import asyncio # Python自带的"异步任务调度器"
from fastapi import FastAPI, HTTPException # FastAPI本体 + 内置的HTTP异常类
from contextlib import asynccontextmanager # 把异步函数变成"上下文管理器"的工具

from forum_app.db.database import Base, engine # 数据库的"图纸(Base)"和"发动机(engine)"
from forum_app.api import forum_api

from fastapi.middleware.cors import CORSMiddleware

from forum_app.utils.exception import (
    http_exception_handler,
    global_exception_handler
)

from contextlib import asynccontextmanager
from infra.nacos.registry import (
    register_service,
    unregister_service
)

# engine 是管道总公司，负责管理和数据库的物理连接。
# Session 是一次办事的上下文，负责记录你要做什么（查哪张表、改哪条数据），最后通过 engine 的管道发命令给 MySQL

# 启动/关闭时间机制
# 这个装饰器把下面的函数变成一个 上下文管理器
# 相当于给函数套上一个壳  进入时做A -> 中间让程序跑 -> 推出时做B
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 在线程池中执行同步的数据库操作，避免阻塞事件循环
    # Base.metadata.create_all 时SQLAlchemy的同步方法 （会卡住时间循环）
    # asyncio.to_thread() 把它扔到后台能线程池里执行，主程序卡死 因为create_all 本身不能 await
    await asyncio.to_thread(Base.metadata.create_all, bind=engine)
    # Base.metadata.create_all(bind=engine)

    await register_service(
        "forum-service",
        8007
    )

    # 交给 Python 的上下文管理器协议，表示"启动完毕，可以开始运行了"
    yield   # 分水岭 之前是启动 之后是关闭

    await unregister_service(
        "forum-service",
        8007
    )

    # 关闭阶段可添加清理逻辑
    engine.dispose() # 关闭数据库连接池，释放资源


app = FastAPI(lifespan=lifespan, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:80",
        "http://127.0.0.1:5173",
        "http://localhost",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

# 处理异常
app.add_exception_handler(
    HTTPException, # 要捕获的异常类型
    http_exception_handler # 处理的异常函数
)

# 兜底处理所有其他 Exception（如代码写错了导致的服务器内部错误 500）
app.add_exception_handler(
    Exception, # 所有异常的基类（最宽泛）
    global_exception_handler # 兜底处理函数
)

app.include_router(
    forum_api.router,
    prefix="/forum",
    tags=["Forum"]
)

# 当有人访问网站的根地址 http://your-site.com/ 时
@app.get("/") # @ 是 Python 装饰器，表示"把下面的函数注册为 GET 接口"
def root(): # 函数名可以随便取，这里叫 root
    return {"message": "OK"} # 返回一个 JSON 字典给客户端