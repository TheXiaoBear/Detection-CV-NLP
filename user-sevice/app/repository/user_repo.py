from sqlalchemy.orm import Session, joinedload
from app.models.user import User

# 新建用户
def create(db: Session, user: User):
    db.add(user)
    return user

# 用id只查用户信息
def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# 根据用户id查询该用户信息
def search_id(db: Session, user_id: int):
    return (db.query(User).options(joinedload(User.tasks)).
            filter(User.id == user_id).first())

# 查找同名or同邮箱用户
def search_name(db: Session, name: str):
    return db.query(User).filter(User.username == name).first()
def search_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# 根据用户名查找用户
def search(db: Session, content: str):
    return db.query(User).filter(User.username.like(f'%{content}%')).all()

# 展示所有用户
def get_all(db: Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit).all()

# 删除用户
def delete(db: Session, user: User):
    db.delete(user)