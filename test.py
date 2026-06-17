from ultralytics import YOLO
# https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt
model = YOLO("cv-service/cv_app/weights/yolov11n.pt")


# import redis
#
# r = redis.Redis(
#     host="192.168.233.135",
#     port=6379,
#     decode_responses=True
# )
#
# r.set("test", "hello redis")
#
# value = r.get("test")
#
# print(value)

import subprocess
import sys
import os
import threading
import time
import signal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
processes = []


def run_service(name, cwd, command, color_code, delay=0):
    """运行服务并实时打印带颜色前缀的日志"""
    prefix = f"\033[{color_code}m[{name}]\033[0m"

    if delay > 0:
        print(f"{prefix} 等待 {delay} 秒后启动...")
        time.sleep(delay)

    print(f"{prefix} 启动中... | 目录: {cwd}")
    print(f"{prefix} 命令: {command}")

    process = subprocess.Popen(
        command,
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding='utf-8'
    )
    processes.append(process)

    for line in iter(process.stdout.readline, ''):
        if line:
            print(f"{prefix} {line}", end='')

    process.stdout.close()
    return_code = process.wait()
    print(f"{prefix} 服务已退出，返回码: {return_code}")


def cleanup(signum=None, frame=None):
    print("\n\033[31m👋 正在停止所有服务...\033[0m")
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=2)
        except:
            p.kill()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, cleanup)

    print("=" * 60)
    print("🚀 正在启动 5 个服务...")
    print("=" * 60)

    # ==========================================
    # 服务配置
    # ==========================================
    services = [

        # ======================
        # Gateway（统一入口）
        # ======================
        {
            "name": "gateway",
            "cwd": BASE_DIR,
            "cmd": "uvicorn gateway.gateway:app --host 127.0.0.1 --port 8080 --reload",
            "color": "31",
            "delay": 0
        },

        # ======================
        # Web 服务
        # ======================
        {
            "name": "user-web",
            "cwd": os.path.join(BASE_DIR, "user-service"),
            "cmd": "python run.py",
            "color": "32",
            "delay": 1
        },
        {
            "name": "cv-web",
            "cwd": os.path.join(BASE_DIR, "cv-service"),
            "cmd": "python run.py",
            "color": "34",
            "delay": 2
        },
        {
            "name": "nlp-web",
            "cwd": os.path.join(BASE_DIR, "nlp-service"),
            "cmd": "python run.py",
            "color": "36",
            "delay": 3
        },

        # ======================
        # 业务服务
        # ======================
        {
            "name": "favorite",
            "cwd": os.path.join(BASE_DIR, "favorite"),
            "cmd": "python run.py",
            "color": "33",
            "delay": 4
        },
        {
            "name": "notice",
            "cwd": os.path.join(BASE_DIR, "notice"),
            "cmd": "python run.py",
            "color": "35",
            "delay": 5
        },

        # ======================
        # workers
        # ======================
        {
            "name": "cv-worker",
            "cwd": os.path.join(BASE_DIR, "cv-service"),
            "cmd": "python -m cv_app.run_worker",
            "color": "94",
            "delay": 6
        },
        {
            "name": "nlp-worker",
            "cwd": os.path.join(BASE_DIR, "nlp-service"),
            "cmd": "python -m nlp_app.run_worker",
            "color": "95",
            "delay": 7
        },
    ]

    threads = []
    for svc in services:
        if not os.path.exists(svc["cwd"]):
            print(f"\033[31m[错误] 目录不存在: {svc['cwd']}\033[0m")
            continue

        t = threading.Thread(
            target=run_service,
            args=(svc["name"], svc["cwd"], svc["cmd"], svc["color"], svc["delay"])
        )
        t.daemon = True
        t.start()
        threads.append(t)

    # 打印服务状态
    time.sleep(2)
    print("\n" + "=" * 60)
    print("✅ 所有服务启动中...")
    print("=" * 60)
    print("   • user-web   : http://localhost:8000")
    print("   • cv-web     : http://localhost:8001")
    print("   • nlp-web    : http://localhost:8002")
    print("   • favorite    : http://localhost:8003")
    print("   • notice    : http://localhost:8004")
    print("   • cv-worker  : RabbitMQ 消费者")
    print("   • nlp-worker : RabbitMQ 消费者")
    print("=" * 60)
    print("\n💡 按 Ctrl+C 可停止所有服务\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()




from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import time
import json

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
SERVICES = {
    "user-service": "http://127.0.0.1:8000",
    "favorite": "http://127.0.0.1:8004",
    "notice": "http://127.0.0.1:8005",
    "models": "http://127.0.0.1:8006",
    "llm": "http://127.0.0.1:8007",
}

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

    if service not in SERVICES:
        raise HTTPException(status_code=404)

    target_url = f"{SERVICES[service]}/{path}"
    print("target_url:", target_url)

    body = await request.body()

    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    headers.pop("connection", None)
    headers.pop("origin", None)

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