def build_prompt(results):

    object_descriptions = []

    for r in results:

        object_descriptions.append(
            f"{r.label}(置信度:{round(r.confidence, 2)})"
        )

    content = "、".join(object_descriptions)

    return f"""
图像中识别到了以下目标：

{content}

请仅根据这些目标，
生成一句简短自然的中文描述。

要求：

1. 不要虚构背景
2. 不要虚构动作
3. 不要出现不存在的场景
4. 不要列表形式
5. 一句话即可
"""