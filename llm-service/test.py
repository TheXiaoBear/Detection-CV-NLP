from core.client import client

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {
            "role": "user",
            "content": "你好"
        }
    ]
)

print(response.choices[0].message.content)