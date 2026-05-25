from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "weights" / "yolov8n.pt"

OUTPUT_DIR = BASE_DIR / "outputs"

BOX_DIR = OUTPUT_DIR / "boxes"

HEATMAP_DIR = OUTPUT_DIR / "heatmaps"

LABEL_DIR = OUTPUT_DIR / "labels"