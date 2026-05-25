from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.result import Result

from app.core.manager import ModelManager
from app.core.prompt import build_prompt
from app.core.redis_client import redis_client


def generate_single_description(
    model,
    tokenizer,
    label,
    confidence
):

    prompt = f"""
目标：

{label}

置信度：

{round(confidence, 2)}

请生成一句简短自然的中文描述。

要求：

1. 不要虚构背景
2. 一句话即可
3. 不要列表形式
"""

    messages = [
        {
            "role": "system",
            "content": "你是一个图像目标描述助手。"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=40,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    generated_ids = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    generated_text = tokenizer.decode(
        generated_ids,
        skip_special_tokens=True
    )

    return generated_text.strip()


def generate_description(
    db: Session,
    task_id: int
):

    # redis
    cache_key = f"task:{task_id}:description"

    cached_description = redis_client.get(cache_key)

    if cached_description:
        return {
            "task_id": task_id,
            "description": cached_description,
            "source": "redis_cache"
        }

    # =========================
    # 1. 查询任务
    # =========================
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise Exception("Task not found")

    # =========================
    # 2. 查询检测结果
    # =========================
    results = db.query(Result).filter(
        Result.task_id == task.id
    ).all()

    if not results:
        raise Exception("No detection result")

    # =========================
    # 3. 构建整体 Prompt
    # =========================
    prompt = build_prompt(results)

    # =========================
    # 4. 获取模型
    # =========================
    model, tokenizer = ModelManager.get_model()

    # =========================
    # 5. Chat Template
    # =========================
    messages = [
        {
            "role": "system",
            "content": "你是一个图像描述助手。"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    ).to(model.device)

    # =========================
    # 6. 模型生成
    # =========================
    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    # =========================
    # 7. 只解码新增部分
    # =========================
    generated_ids = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    generated_text = tokenizer.decode(
        generated_ids,
        skip_special_tokens=True
    ).strip()

    # =========================
    # 8. 更新 task.description
    # =========================
    task.description = generated_text
    redis_client.set(
        cache_key,
        generated_text,
        ex=3600
    )
    # =========================
    # 9. 更新 result.sentence
    # =========================
    for result in results:

        sentence = generate_single_description(
            model,
            tokenizer,
            result.label,
            result.confidence
        )

        result.sentence = sentence

    # =========================
    # 10. 提交数据库
    # =========================
    db.commit()

    # =========================
    # 11. 返回
    # =========================
    return {
        "task_id": task.id,
        "description": generated_text
    }