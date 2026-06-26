from v2.nacos import (
    ClientConfigBuilder,
    NacosNamingService,
    RegisterInstanceParam,
    DeregisterInstanceParam,
    ListInstanceParam
)


class NacosClient:

    def __init__(
            self,
            server_addr="127.0.0.1:8848",
            username="nacos",
            password="123456"
    ):

        self.client_config = (
            ClientConfigBuilder()
            .server_address(server_addr)
            .username(username)
            .password(password)
            .build()
        )

    async def naming_service(self):
        return await NacosNamingService.create_naming_service(
            self.client_config
        )

    async def register(
            self,
            service_name,
            ip,
            port
    ):

        service = await self.naming_service()

        await service.register_instance(
            RegisterInstanceParam(
                service_name=service_name,
                ip=ip,
                port=port
            )
        )

    async def unregister(
            self,
            service_name,
            ip,
            port
    ):

        service = await self.naming_service()

        await service.deregister_instance(
            DeregisterInstanceParam(
                service_name=service_name,
                ip=ip,
                port=port
            )
        )

    async def get_instances(
            self,
            service_name
    ):

        service = await self.naming_service()

        return await service.list_instances(
            ListInstanceParam(
                service_name=service_name,
            healthy_only=True
            )
        )