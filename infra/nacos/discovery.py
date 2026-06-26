from infra.nacos.client import NacosClient

nacos = NacosClient()


async def discover(service_name: str):

    instances = await nacos.get_instances(
        service_name
    )

    if not instances:
        raise Exception(
            f"{service_name} 不存在"
        )

    return instances[0]