import socket

from infra.nacos.client import NacosClient


nacos = NacosClient()


async def register_service(
        service_name: str,
        port: int
):

    ip = socket.gethostbyname(
        socket.gethostname()
    )

    await nacos.register(
        service_name=service_name,
        ip=ip,
        port=port
    )

    print(
        f"[Nacos] {service_name} 注册成功 "
        f"{ip}:{port}"
    )


async def unregister_service(
        service_name: str,
        port: int
):

    ip = socket.gethostbyname(
        socket.gethostname()
    )

    await nacos.unregister(
        service_name=service_name,
        ip=ip,
        port=port
    )

    print(
        f"[Nacos] {service_name} 已注销"
    )

async def discover_service(
        service_name: str
):
    instances = await nacos.get_instances(
        service_name
    )

    if not instances:
        raise Exception(
            f"{service_name} 不存在"
        )

    instance = instances[0]

    return {
        "ip": instance.ip,
        "port": instance.port
    }