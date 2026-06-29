import redis
from infra.nacos.settings import settings

redis_client = redis.Redis(
    host="192.168.233.135",
    port=6379,
    decode_responses=True
)
# redis_client = redis.Redis(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     # password=settings.REDIS_PASSWORD,
#     decode_responses=True
# )
