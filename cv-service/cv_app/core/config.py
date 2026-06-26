from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


MODEL_PATHS = {

    "yolov8n": BASE_DIR / "weights" / "yolov8n.pt",

    "yolov11n": BASE_DIR / "weights" / "yolov11n.pt",

    "yolov5su": BASE_DIR / "weights" / "yolov5su.pt",

    "custom": BASE_DIR / "weights" / "custom.pt",
}


OUTPUT_DIR = BASE_DIR / "outputs"

BOX_DIR = OUTPUT_DIR / "boxes"

HEATMAP_DIR = OUTPUT_DIR / "heatmaps"

LABEL_DIR = OUTPUT_DIR / "labels"