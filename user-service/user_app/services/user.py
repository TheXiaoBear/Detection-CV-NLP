from sqlalchemy.orm import Session

from user_app.models.user import User
from user_app.schemas.user import UserCreate, UserUpdate
from user_app.repository import user_repo
from user_app.utils.security import hash_password, verify_password
from fastapi import HTTPException

from user_app.utils.page import PageMethod


# 关于commit
# 把当前 Session（会话）中所有挂起的改动，一次性真正写入数据库  这里的挂起代表 改动已记录但未执行
# 因为 database.py 里设置了 autocommit=False。SQLAlchemy 不会自动帮你保存，必须手动喊一声"存档"
# 关于refresh
# 重新去数据库查一遍这条记录的最新数据，把结果回填到 user 这个 Python 对象里
# 去数据库把这条记录的最新完整版拿回来，更新我的本地对象
# 关于rollback
# 撤销当前事务中所有未提交的改动，让数据库回到本次事务开始前的状态

# 新建用户
def create_user(db: Session, user_in: UserCreate):
    try:

        username_exists = user_repo.search_name(
            db,
            user_in.username
        )

        if username_exists:
            raise HTTPException(
                status_code=400,
                detail="用户名已经存在"
            )

        email_exists = user_repo.search_email(
            db,
            user_in.email
        )

        if email_exists:
            raise HTTPException(
                status_code=400,
                detail="邮箱已被注册"
            )

        user = User(
            username=user_in.username,
            password=hash_password(user_in.password),
            email=user_in.email
        )

        user_repo.create(db, user)

        db.commit()

        db.refresh(user)

        return user

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="服务器内部错误"
        )

# 查某一用户 信息
def get_user(db: Session, user_id: int):
    user = user_repo.search_id(db, user_id)

    if not user:
        raise HTTPException(404, "User not found")

    return user

# 查询所有用户
def get_users(page: PageMethod ,db: Session):
    skip = (page.page_num - 1) * page.page_size

    return user_repo.get_all(db, skip, limit = page.page_size)

# 更新用户
def update_user(db: Session, user_id: int, user_in: UserUpdate):
    user = get_user(db, user_id)

    if not user:
        return None

    # ======================
    # username 重复检查
    # ======================
    if user_in.username:
        exist = db.query(User).filter(
            User.username == user_in.username,
            User.id != user_id
        ).first()

        if exist:
            raise HTTPException(400, "用户名已存在")

    for k, v in user_in.model_dump(exclude_unset=True).items():
        setattr(user, k, v)

    db.commit()
    db.refresh(user)

    return user

# 更新用户头像
def update_avatar(db: Session, user_id: int, avatar: str):
    user = get_user(db, user_id)

    if not user:
        return None

    user.avatar = avatar

    db.commit()
    db.refresh(user)

    return user

# 删除用户
def delete_user(db: Session, user_id: int):

    user = get_user(db, user_id)

    user_repo.delete(db, user)

    db.commit()

# 更改密码
def change_password(db: Session, user_id: int, current_password: str, new_password: str):
    user = get_user(db, user_id)

    # 校验旧密码
    if not verify_password(current_password, user.password):
        raise HTTPException(status_code=400, detail="密码与原密码不符")

    # 新密码重新hash
    user.password = hash_password(new_password)

    db.commit()
    db.refresh(user)

    return user

# 登录时查用户名
def get_user_by_username(
    db: Session,
    username: str
):

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

def soft_delete_user(db: Session, user_id: int):

    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user_repo.soft_delete(db, user)

    db.commit()
    db.refresh(user)

    return user


def hard_delete_user(db: Session, user_id: int):

    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user_repo.hard_delete(db, user)

    db.commit()

def restore_delete_user(db: Session, user_id: int):

    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user_repo.restore_delete(db, user)

    db.commit()
    db.refresh(user)

    return user


def search_user(db: Session, username,  page_num, page_size):
    
    skip = (page_num - 1) * page_size
    query = user_repo.get_all(db, skip, limit = page_size)

    if username is not None and username.strip() != "":
        query = user_repo.search(db, username)

    total = query.count()

    records = query.offset(skip).limit(page_size).all()

    return {
        "records": records,
        "totalRow": total
    }