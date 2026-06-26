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
    def chat(messages):

        if isinstance(messages, str):

            messages = [
                {
                    "role": "user",
                    "content": messages
                }
            ]

        response = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content

    @staticmethod
    def stream_chat(messages):
        print("==========进入路由==========")

        if isinstance(messages, str):

            messages = [
                {
                    "role": "user",
                    "content": messages
                }
            ]

        response = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            stream=True
        )

        print("==========开始调用Qwen==========")
        for chunk in response:

            print("原始chunk:", chunk)

            if (
                    chunk.choices
                    and chunk.choices[0].delta.content
            ):
                content = chunk.choices[0].delta.content

                print("content:", repr(content))

                yield content