import redis


redis_client = redis.Redis(
    host="192.168.233.135",
    port=6379,
    decode_responses=True
)