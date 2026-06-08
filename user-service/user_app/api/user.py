from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from user_app.db.database import get_db
from user_app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin, User_to_Task, ChangePassword
from user_app.services import user as user_service
from user_app.utils.auth import require_admin, get_current_user
from user_app.utils.security import verify_password
from user_app.utils.jwt import create_access_token
from user_app.utils.response import ResponseUtil
from user_app.utils.oss import upload_file
from user_app.utils.page import PageMethod
from user_app.core.redis_client import redis_client
from typing import Optional
router = APIRouter()

# 注册
@router.post("/users", response_model=UserResponse)
def create_user(users: UserCreate, db: Session = Depends(get_db)):
    return ResponseUtil.success(user_service.create_user(db, users))

# 获取全部用户
@router.get("/users", response_model=list[UserResponse])
def list_users(page: PageMethod,db: Session = Depends(get_db), current_user  = Depends(require_admin)):
    return ResponseUtil.success(user_service.get_users(page, db))

# 查询某一用户相关信息
@router.get("/users/me", response_model=User_to_Task)
def get_user(db: Session = Depends(get_db), current_user  = Depends(get_current_user)):
    user_id = current_user["user_id"]
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return ResponseUtil.success(data=user)

# 更新用户信息
@router.put("/users/change", response_model=UserResponse)
def update_user(user: UserUpdate,
                db: Session = Depends(get_db), current_user  = Depends(get_current_user)):
    user_id = current_user["user_id"]
    result = user_service.update_user(db, user_id, user)
    if not result:
        raise HTTPException(404, "User not found")
    return ResponseUtil.success(data=result)

# 更新用户头像
@router.put("/users/avatar")
async def update_avatar(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    contents = await image.read()

    avatar = upload_file(
        contents,
        image.filename
    )
    print(avatar)
    user = user_service.update_avatar(
        db,
        current_user["user_id"],
        avatar
    )

    if not user:
        raise HTTPException(404, "User not found")

    return ResponseUtil.success(data={
        "avatar": avatar
    },message="头像更新成功")


# 删除用户 注销
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db),  current_user  = Depends(get_current_user)):
    result = user_service.delete_user(db, user_id)
    if not result:
        raise HTTPException(404, "删除失败")
    return {"message": "删除成功"}


# 登录 还得校验token对不对，免得乱写一个token就能使用
@router.post("/login")
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db)
):
    user = user_service.get_user_by_username(
        db,
        user_in.username
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="用户名错误"
        )

    if not verify_password(
        user_in.password,
        user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="密码错误"
        )

    # 生成jwt
    token = create_access_token({
        "user_id": user.id,
        "avatar": user.avatar,
        "role": user.role
    })

    # redis key
    redis_key = f"user:{user.id}:token"

    # =========================
    # 存 Redis
    # ex=3600 表示1小时过期
    # =========================
    redis_client.set(
        redis_key,
        token,
        ex=3600
    )

    return ResponseUtil.success(
        data={
            "token": token,
            "type": "bearer"
        },
        message="登录成功"
    )

# 登出
@router.post("/logout")
def logout(
    current_user = Depends(get_current_user)
):

    user_id = current_user["user_id"]

    redis_key = f"user:{user_id}:token"

    redis_client.delete(redis_key)

    return ResponseUtil.success(message="登出成功")

# 修改密码
@router.put("/users/change")
def change_password(password: ChangePassword, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    user_id = current_user["user_id"]
    result = user_service.change_password(db, user_id, password.current_password, password.new_password)
    if not result:
        raise HTTPException(404, '没找到用户或密码错误')
    return ResponseUtil.success(data=result)

# 搜素用户
@router.get('/users/search')
def search_users(username: Optional[str] = None,
                 page_num: int = 1,current_user = Depends(require_admin),
                page_size: int = 10, db: Session = Depends(get_db),
                 ):
    return ResponseUtil.success(user_service.search_user(db, username, page_num, page_size))

# 硬删除
@router.delete("/users/delete_hard/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = user_service.hard_delete_user(db, user_id)
    if not result:
        raise HTTPException(404, "User not found")
    return ResponseUtil.success(message="永久删除")

# 账号封禁 软删除
@router.put("/users/delete_soft/{user_id}")
def soft_delete_user(user_id: int, db: Session = Depends(get_db)):
    result = user_service.soft_delete_user(db, user_id)

    if not result:
        raise HTTPException(404, "User not found")

    return ResponseUtil.success(data="成功", code=200,
        message="软删除成功"
    )

# 删除恢复
@router.put("/users/recover/{user_id}")
def recover_user(user_id: int, db: Session = Depends(get_db)):
    result = user_service.restore_delete_user(db, user_id)

    if not result:
        raise HTTPException(404, "User not found")

    return ResponseUtil.success(message="恢复成功")
