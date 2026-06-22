from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from llm_app.db.database import Base
from llm_app.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship


# 此处准备一个报告管理页面，一个更新按钮，对数据库内的数据进行一个处理得出以下数据
class Evaluation(Base, TimestampMixin):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey("tasks.id"), unique=True)

    precision = Column(Float) # 精确率 (0-1) 检出来的有多准
    recall = Column(Float) # 召回率 (0-1) 有多少漏掉了

    f1 = Column(Float) # F1分数 (0-1) 平衡两者

    map50 = Column(Float) # mAP@50 (0-1) 宽松标准下的综合能力

    map50_95 = Column(Float) # mAP@50-95 (0-1) 严格标准下的综合能力（更权威）

    model_name = Column(String(50))

    inference_time = Column(Float) #  单张推理时间（毫秒）

