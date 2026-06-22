import os

from openai import OpenAI
from dotenv import load_dotenv

from llm_app.core.config import settings

# load_dotenv()
# QWEN_API_KEY = os.getenv("QWEN_API_KEY")

client = OpenAI(
    api_key=settings.QWEN_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


class QwenClient:

    @staticmethod
    def stream_chat(messages):
        print("messages=")
        print(messages)
        response = (
            client.chat.completions.create(
                model="qwen-plus",
                messages=messages,
                stream=True
            )
        )

        for chunk in response:

            if (
                chunk.choices
                and chunk.choices[0].delta.content
            ):

                yield (
                    chunk
                    .choices[0]
                    .delta.content
                )