from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.task import TaskUpdate, TaskResponse
from app.services import task as task_service
from app.utils.oss import upload_file
from app.utils.page import PageMethod
from app.mq.producer import send_cv_task


router = APIRouter()

# 上传图片（新建图片样本）
@router.post("/tasks")
async def create_task(
    user_id: int = Form(...),
    image_path: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    image_url = None

    if image_path:
        file_bytes = await image_path.read()
        image_url = upload_file(
            file_bytes,
            image_path.filename
        )
    task = task_service.create_task(
        db=db,
        user_id=user_id,
        image_path=image_url,
    )

    # 发送到MQ
    # send_nlp_task(task.id)
    send_cv_task(task.id)
    return task

# 获取所有事物
@router.get("/tasks")
async def get_tasks(page: PageMethod ,db: Session = Depends(get_db)):
    return task_service.get_tasks(page, db)

# 获取当前用户的记录 以及对当前记录查询
@router.get("/tasks/search/{user_id}", response_model=TaskResponse)
def read_task(title: str, user_id: int, page: PageMethod, db: Session = Depends(get_db)):
    return task_service.get_task(title, user_id, page, db)

# 更新对应项信息
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task(db, task_id, task)

# 硬删除
@router.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    result = task_service.hard_delete_task(db, task_id)
    if not result:
        raise HTTPException(404, "Task not found")
    return {"message": "deleted"}

# 软删除
@router.put("/tasks/{task_id}/delete")
def soft_delete_task(task_id: int, db: Session = Depends(get_db)):
    result = task_service.soft_delete_task(db, task_id)

    if not result:
        raise HTTPException(404, "Task not found")

    return {"message": "task soft deleted"}