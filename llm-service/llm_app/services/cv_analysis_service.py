from collections import defaultdict

from sqlalchemy.orm import Session

from llm_app.models.result import Result
from llm_app.models.task import Task
from llm_app.models.evaluation import Evaluation


class CVAnalysisService:

    LOW_CONF_THRESHOLD = 0.7

    @staticmethod
    def build(task_id: int, db: Session):

        results = (
            db.query(Result)
            .filter(Result.task_id == task_id)
            .all()
        )

        if not results:
            return {}

        statistics = defaultdict(list)

        for item in results:

            width = max(item.x2 - item.x1, 0)
            height = max(item.y2 - item.y1, 0)

            area = width * height

            statistics[item.label].append(
                {
                    "confidence": item.confidence,
                    "area": area
                }
            )

        task = (
            db.query(Task)
            .filter(Task.id == task_id)
            .first()
        )

        evaluation = (
            db.query(Evaluation)
            .filter(
                Evaluation.task_id == task_id
            )
            .first()
        )



        analysis = {
            "task": {
                "task_id": task.id,
                "title": task.title,
                "cv_model": task.cv_model,
                "cv_duration": task.cv_duration,
                "confidence": task.confidence
            },

            "evaluation": {

            "precision":
                evaluation.precision
                if evaluation else None,

            "recall":
                evaluation.recall
                if evaluation else None,

            "f1":
                evaluation.f1
                if evaluation else None,

            "map50":
                evaluation.map50
                if evaluation else None,

            "map50_95":
                evaluation.map50_95
                if evaluation else None,

            "inference_time":
                evaluation.inference_time
                if evaluation else None,

            "model_name":
                evaluation.model_name
                if evaluation else None
        },

            "detections": {}
        }
        for label, items in statistics.items():

            confidences = [
                x["confidence"]
                for x in items
            ]

            areas = [
                x["area"]
                for x in items
            ]

            low_conf_count = sum(
                1
                for conf in confidences
                if conf < CVAnalysisService.LOW_CONF_THRESHOLD
            )

            analysis[label] = {

                "count": len(items),

                "avg_confidence": round(
                    sum(confidences) / len(confidences),
                    4
                ),

                "max_confidence": round(
                    max(confidences),
                    4
                ),

                "min_confidence": round(
                    min(confidences),
                    4
                ),

                "low_conf_ratio": round(
                    low_conf_count / len(items),
                    4
                ),

                "avg_area": round(
                    sum(areas) / len(areas),
                    2
                )
            }

        return analysis