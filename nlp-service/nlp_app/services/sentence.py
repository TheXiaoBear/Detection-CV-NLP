import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import time

from sqlalchemy.orm import Session

from nlp_app.models.task import Task
from nlp_app.models.result import Result

from nlp_app.core.manager import ModelManager
from nlp_app.core.redis_client import redis_client

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "weights",
        "textcnn_scene_model.pth"
    )
)
COCO_CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic_light', 'fire_hydrant', 'stop_sign', 'parking_meter', 'bench', 'bird', 'cat',
    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports_ball',
    'kite', 'baseball_bat', 'baseball_glove', 'skateboard', 'surfboard', 'tennis_racket',
    'bottle', 'wine_glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot_dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted_plant', 'bed', 'dining_table', 'toilet', 'tv', 'laptop',
    'mouse', 'remote', 'keyboard', 'cell_phone', 'microwave', 'oven', 'toaster', 'sink',
    'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy_bear', 'hair_drier', 'toothbrush'
]
WORD_TO_IDX = {word: i + 1 for i, word in enumerate(COCO_CLASSES)}
WORD_TO_IDX['<PAD>'] = 0

SCENES = [
    "urban_street",
    "park",
    "bedroom",
    "kitchen",
    "office",
    "living_room",
    "shopping_mall",
    "sports_field"
]

IDX_TO_LABEL = {
    i: scene
    for i, scene in enumerate(SCENES)
}

SCENE_CN = {
    "urban_street": "城市道路",
    "park": "公园",
    "bedroom": "卧室",
    "kitchen": "厨房",
    "office": "办公室",
    "living_room": "客厅",
    "shopping_mall": "商场",
    "sports_field": "运动场"
}

MAX_LEN = 16

class LocalTextCNN(nn.Module):
    def __init__(
        self,
        vocab_size=81,
        embedding_dim=128,
        num_classes=8,
        filter_sizes=None,
        num_filters=100
    ):
        if filter_sizes is None:
            filter_sizes = [2, 3, 4]
        super(LocalTextCNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.convs = nn.ModuleList([nn.Conv2d(1, num_filters, (fs, embedding_dim)) for fs in filter_sizes])
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(len(filter_sizes) * num_filters, num_classes)

    def forward(self, x):
        x = self.embedding(x).unsqueeze(1)

        pooled_outputs = []

        for conv in self.convs:
            act = F.relu(
                conv(x)
            )

            pooled = F.max_pool2d(
                act,
                (act.shape[2], 1)
            )

            pooled_outputs.append(
                pooled.squeeze(3).squeeze(2)
            )

        features = torch.cat(
            pooled_outputs,
            dim=1
        )

        features = self.dropout(
            features
        )

        return self.fc(
            features
        )

# 单例模式在内存中加载一次 TextCNN 权重，不影响原模型的启动速度
_textcnn_instance = None

def get_local_textcnn():
    global _textcnn_instance
    if _textcnn_instance is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = LocalTextCNN()
        # 💡 确保你的 'textcnn_scene_model.pth' 放在项目能读到的路径下（这里使用相对或绝对路径均可）
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"TextCNN模型不存在: {MODEL_PATH}"
            )
        model.load_state_dict(
            torch.load(
                MODEL_PATH,
                map_location=device
            )
        )
        model.to(device)
        model.eval()
        _textcnn_instance = model
    return _textcnn_instance

def predict_scene(results):
    labels = []

    labels = list(
        dict.fromkeys(
            res.label.replace(" ", "_")
            for res in results
        )
    )

    text_input = " ".join(labels)

    tokens = [
        WORD_TO_IDX.get(
            word,
            0
        )
        for word in text_input.split()
    ]

    if len(tokens) < MAX_LEN:
        tokens += [0] * (MAX_LEN - len(tokens))
    else:
        tokens = tokens[:MAX_LEN]

    textcnn_model = get_local_textcnn()

    device = next(
        textcnn_model.parameters()
    ).device

    input_tensor = torch.tensor(
        [tokens],
        dtype=torch.long
    ).to(device)

    with torch.no_grad():

        t0 = time.perf_counter()
        logits = textcnn_model(
            input_tensor
        )
        t1 = time.perf_counter()
        nlp_duration = t1 - t0

        probs = F.softmax(
            logits,
            dim=1
        )

        confidence, predicted_idx = torch.max(
            probs,
            dim=1
        )

    scene = IDX_TO_LABEL[
        predicted_idx.item()
    ]

    return {
        "scene": scene,
        "scene_cn": SCENE_CN[scene],
        "confidence": confidence.item(),
        "duration": nlp_duration,
    }

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

    # t0 = time.perf_counter()
    outputs = model.generate(
        **inputs,
        max_new_tokens=40,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )
    # t1 = time.perf_counter()
    # llm_duration = t1 - t0

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
    # prompt = build_prompt(results)

    # =========================
    # 4. 获取模型
    # =========================
    model, tokenizer = ModelManager.get_model()

    # # =========================
    # # 5. Chat Template
    # # =========================
    # messages = [
    #     {
    #         "role": "system",
    #         "content": "你是一个图像描述助手。"
    #     },
    #     {
    #         "role": "user",
    #         "content": prompt
    #     }
    # ]
    #
    # text = tokenizer.apply_chat_template(
    #     messages,
    #     tokenize=False,
    #     add_generation_prompt=True
    # )
    #
    # inputs = tokenizer(
    #     text,
    #     return_tensors="pt"
    # ).to(model.device)
    #
    # # =========================
    # # 6. 模型生成
    # # =========================
    # outputs = model.generate(
    #     **inputs,
    #     max_new_tokens=80,
    #     temperature=0.7,
    #     top_p=0.9,
    #     do_sample=True
    # )
    #
    # # =========================
    # # 7. 只解码新增部分
    # # =========================
    # generated_ids = outputs[0][
    #     inputs["input_ids"].shape[1]:
    # ]
    #
    # generated_text = tokenizer.decode(
    #     generated_ids,
    #     skip_special_tokens=True
    # ).strip()
    unique_labels = {
        result.label.replace(" ", "_")
        for result in results
    }

    duration = 0.0
    scene_confidence = 0.0

    if len(unique_labels) <= 1:

        generated_text = "目标类别数量不足，跳过场景识别"

        print(
            f"[TextCNN] task={task_id} "
            f"目标类别数量不足，跳过场景识别"
        )

    else:

        scene_result = predict_scene(results)

        duration = float(
            scene_result["duration"]
        )

        scene_confidence = float(
            scene_result["confidence"]
        )

        generated_text = (
            f"识别场景：{scene_result['scene_cn']}"
            f"（置信度：{scene_confidence * 100:.2f}%）"
        )

        print(
            f"[TextCNN] "
            f"scene={scene_result['scene_cn']} "
            f"confidence={scene_confidence:.4f}"
        )

    # =========================
    # 8. 更新 task.description
    # =========================
    task.description = generated_text
    task.status = "NLP_success"
    task.nlp_duration = round(duration, 4)
    task.nlp_model = "TextCNN"
    task.confidence = round(scene_confidence, 4)
    redis_client.set(
        cache_key,
        generated_text,
        ex=3600
    )
    # =========================
    # 9. 更新 result.sentence
    # =========================
    label_cache = {}

    for result in results:

        label_key = result.label.strip().lower()

        if label_key not in label_cache:
            label_cache[result.label] = (
                generate_single_description(
                    model,
                    tokenizer,
                    result.label,
                    result.confidence
                )
            )

        result.sentence = label_cache[result.label]

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