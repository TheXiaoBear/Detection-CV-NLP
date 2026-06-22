from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class PromptManager:

    @staticmethod
    def load(name: str):

        path = BASE_DIR / "prompts" / f"{name}.txt"

        with open(
                path,
                "r",
                encoding="utf-8"
        ) as f:

            return f.read()