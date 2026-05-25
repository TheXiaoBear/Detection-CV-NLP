import cv2
import numpy as np


def generate_heatmap(image, results):

    """
    image:
        原图 numpy 数组

    results:
        YOLO 推理结果
    """

    # 创建热力图画布
    heatmap = np.zeros(
        image.shape[:2],
        dtype=np.float32
    )

    # 遍历检测框
    for box in results[0].boxes:

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0]
        )

        confidence = float(box.conf[0])

        # 在框区域叠加热度
        heatmap[y1:y2, x1:x2] += confidence

    # 归一化
    heatmap = cv2.normalize(
        heatmap,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    heatmap = heatmap.astype(np.uint8)

    # 伪彩色
    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    # 与原图融合
    overlay = cv2.addWeighted(
        image,
        0.6,
        heatmap,
        0.4,
        0
    )

    return overlay