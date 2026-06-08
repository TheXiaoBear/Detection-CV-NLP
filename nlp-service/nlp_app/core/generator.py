LABEL_MAP = {
    "cat": "检测到一只猫",
    "dog": "检测到一只狗",
    "person": "检测到一个人",
    "car": "检测到一辆汽车"
}


def generate_sentence(label: str):

    return LABEL_MAP.get(
        label,
        f"检测到目标 {label}"
    )