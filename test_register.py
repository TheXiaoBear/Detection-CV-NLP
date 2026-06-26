import asyncio
import socket

from infra.nacos.client import NacosClientWrapper


async def main():

    client = NacosClientWrapper()

    ip = socket.gethostbyname(
        socket.gethostname()
    )

    await client.register(
        service_name="user-service",
        ip=ip,
        port=8000
    )

    print("注册成功")

    while True:
        await asyncio.sleep(10)


asyncio.run(main())