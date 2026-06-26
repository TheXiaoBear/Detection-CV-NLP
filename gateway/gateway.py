from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import time
import json
from fastapi.responses import StreamingResponse
from infra.nacos.discovery import discover


app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# SERVICES
# =========================
# SERVICES = {
#     "user-service": "http://127.0.0.1:8000",
#     "favorite": "http://127.0.0.1:8004",
#     "notice": "http://127.0.0.1:8005",
#     "models": "http://127.0.0.1:8006",
#     "llm": "http://127.0.0.1:8003",
# }

# =========================
# OPTIONS DEBUG
# =========================
@app.options("/{service}/{path:path}")
async def options_debug(service: str, path: str, request: Request):
    print("\n========== OPTIONS ==========")
    print("service:", service)
    print("path:", path)
    print("origin:", request.headers.get("origin"))
    print("headers:", dict(request.headers))
    print("=============================\n")

    return Response(
        status_code=204,
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

# =========================
# MAIN PROXY
# =========================
@app.api_route(
    "/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def proxy(service: str, path: str, request: Request):

    print("\n========== REQUEST ==========")
    print("method:", request.method)
    print("service:", service)
    print("path:", path)
    print("raw url:", str(request.url))

    # if service not in SERVICES:
    #     raise HTTPException(status_code=404)
    #
    # # 前缀只作为识别，不作为url的一部分
    # target_url = f"{SERVICES[service]}/{path}"

    try:
        instance = await discover(service)

    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"服务 {service} 不存在"
        )

    target_url = (
        f"http://{instance.ip}:{instance.port}/{path}"
    )
    print("target_url:", target_url)

    body = await request.body()

    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    headers.pop("connection", None)
    headers.pop("origin", None)

    if service == "llm" and path == "chat/stream":

        client = httpx.AsyncClient(timeout=None)

        async def stream_generator():

            try:

                req = client.build_request(
                    request.method,
                    target_url,
                    headers=headers,
                    params=request.query_params,
                    content=body
                )

                resp = await client.send(
                    req,
                    stream=True
                )

                async for chunk in resp.aiter_text():
                    yield chunk

            finally:

                await resp.aclose()
                await client.aclose()

        return StreamingResponse(
            stream_generator(),
            media_type="text/plain"
        )

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=request.query_params,
            content=body
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers)
    )