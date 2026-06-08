from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from user_app.db.database import get_db
from user_app.schemas.task import TaskUpdate, TaskResponse, StartTaskRequest
from user_app.services import task as task_service
from user_app.utils.oss import upload_file
from user_app.utils.page import PageMethod
from user_app.mq.producer import send_cv_task
from user_app.utils.auth import require_admin, get_current_user
from user_app.utils.response import ResponseUtil


router = APIRouter()

# 上传图片（新建图片样本）
@router.post("/tasks")
async def create_task(
    current_user = Depends(get_current_user),
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
        user_id=current_user["user_id"],
        image_path=image_url,
    )

    return ResponseUtil.success(task)


@router.post("/tasks/{task_id}/start")
def start_detect(
    task_id: int,
    model_name: StartTaskRequest,
    db: Session = Depends(get_db)
):
    send_cv_task(task_id, model_name.model_name)

    return ResponseUtil.success(data="成功", code=200,
        message="任务已进入检测队列"
    )

# 获取所有事物
@router.get("/tasks")
async def get_tasks(page: PageMethod , current_user = Depends(require_admin),db: Session = Depends(get_db)):
    return task_service.get_tasks(page, db)

# 获取当前用户的记录 以及对当前记录查询
@router.get("/tasks/search")
def search_my_tasks(
    title: Optional[str] = None,
    page_num: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return ResponseUtil.success(task_service.get_task(
        db=db,
        title=title,
        user_id=current_user["user_id"],
        page_num=page_num,
        page_size=page_size
        ))

# 关联搜素当前task的信息和其所对应的result
@router.get("/tasks/to_result")
def search_task_result(task_id: int, db: Session = Depends(get_db)):
    return ResponseUtil.success(task_service.task_result(db=db, task_id=task_id))

# 更新对应项信息
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return ResponseUtil.success(task_service.update_task(db, task_id, task))



# 硬删除
@router.delete("/tasks/delete_hard/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    result = task_service.hard_delete_task(db, task_id)
    if not result:
        raise HTTPException(404, "Task not found")
    return ResponseUtil.success(message="永久删除")

# 软删除
@router.put("/tasks/delete_soft/{task_id}")
def soft_delete_task(task_id: int, db: Session = Depends(get_db)):
    result = task_service.soft_delete_task(db, task_id)

    if not result:
        raise HTTPException(404, "Task not found")

    return ResponseUtil.success(data="成功", code=200,
        message="软删除成功"
    )

# 删除恢复
@router.put("/tasks/recover/{task_id}")
def recover_task(task_id: int, db: Session = Depends(get_db)):
    result = task_service.restore_delete_task(db, task_id)

    if not result:
        raise HTTPException(404, "Task not found")

    return ResponseUtil.success(message="恢复成功")

# 获取所有被删除事物
@router.get("/tasks/delete")
async def get_tasks(page: PageMethod ,db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return ResponseUtil.success(task_service.get_tasks_delete(page, user_id=current_user["user_id"], db=db))

# 搜素被删除的事物
@router.get("/tasks/search_delete")
def search_my_tasks_delete(
    title: Optional[str] = None,
    page_num: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return ResponseUtil.success(task_service.get_delete_task(
        db=db,
        title=title,
        user_id=current_user["user_id"],
        page_num=page_num,
        page_size=page_size
        ))
