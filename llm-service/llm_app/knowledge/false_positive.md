误检(False Positive)是目标检测常见问题。

常见原因：

1. 背景纹理与目标相似
2. 类别边界模糊
3. 数据集负样本不足

优化方法：

1. 增加负样本
2. 提高confidence阈值
3. 使用Focal Loss