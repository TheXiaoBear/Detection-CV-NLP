from pathlib import Path
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
import torch


class ModelManager:

    tokenizer = None
    model = None

    @classmethod
    def get_model(cls):

        if cls.model is not None:
            return cls.model, cls.tokenizer

        cls.load_model()

        return cls.model, cls.tokenizer

    @classmethod
    def load_model(cls):

        base_dir = Path(__file__).resolve().parent

        model_path = (
            base_dir.parent
            / "weights"
            / "qwen"
        )

        print(f"[DEBUG] loading model from: {model_path}")

        cls.tokenizer = AutoTokenizer.from_pretrained(
            str(model_path),
            local_files_only=True
        )

        cls.model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            torch_dtype=torch.float16,
            device_map="auto",
            local_files_only=True
        )