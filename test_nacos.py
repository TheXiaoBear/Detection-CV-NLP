import asyncio

from infra.nacos.registry import nacos


async def main():
    result = await nacos.get_instances(
        "user-service"
    )

    print(result)


asyncio.run(main())