import subprocess
import sys
import os
import threading
import time
import signal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
processes = []


def run_service(name, cwd, command, color_code, delay=0):
    """运行服务，保持 TTY 以支持热重载，同时添加颜色前缀"""
    prefix = f"\033[{color_code}m[{name}]\033[0m"

    if delay > 0:
        print(f"{prefix} 等待 {delay} 秒后启动...")
        time.sleep(delay)

    print(f"{prefix} 启动中... | 目录: {cwd}")
    print(f"{prefix} 命令: {command}")

    # 方案A：直接启动，不捕获输出（保留 TTY，热重载正常）
    # 但无法添加颜色前缀
    # process = subprocess.Popen(command, cwd=cwd, shell=True)

    # 方案B：使用伪终端（Windows 需要特殊处理，较复杂）

    # 方案C：捕获输出但修复编码，同时用环境变量强制 UTF-8
    # 这是折中方案：热重载可能仍受限，但至少不会崩溃

    # 强制子进程使用 UTF-8
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    process = subprocess.Popen(
        command,
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding='utf-8',  # 尝试 UTF-8
        errors='replace',  # 无法解码时用 � 替换，不崩溃
        env=env
    )
    processes.append(process)

    for line in iter(process.stdout.readline, ''):
        if line:
            print(f"{prefix} {line}", end='')

    process.stdout.close()
    return_code = process.wait()
    print(f"{prefix} 服务已退出，返回码: {return_code}")


def cleanup(signum=None, frame=None):
    print("\n\033[31m 正在停止所有服务...\033[0m")
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
    print(" 正在启动服务...")
    print("=" * 60)

    services = [
        {
            "name": "gateway",
            "cwd": BASE_DIR,
            "cmd": "uvicorn gateway.gateway:app --host 127.0.0.1 --port 8080 --reload",
            "color": "31",
            "delay": 0
        },
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
        {
            "name": "llm",
            "cwd": os.path.join(BASE_DIR, "llm-service"),
            "cmd": "python run.py",
            "color": "36",
            "delay": 4
        },
        {
            "name": "favorite",
            "cwd": os.path.join(BASE_DIR, "favorite"),
            "cmd": "python run.py",
            "color": "33",
            "delay": 5
        },
        {
            "name": "notice",
            "cwd": os.path.join(BASE_DIR, "notice"),
            "cmd": "python run.py",
            "color": "35",
            "delay": 6
        },
        {
            "name": "cv-worker",
            "cwd": os.path.join(BASE_DIR, "cv-service"),
            "cmd": "python -m cv_app.run_worker",
            "color": "94",
            "delay": 7
        },
        {
            "name": "nlp-worker",
            "cwd": os.path.join(BASE_DIR, "nlp-service"),
            "cmd": "python -m nlp_app.run_worker",
            "color": "95",
            "delay": 8
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

    time.sleep(2)
    print("\n" + "=" * 60)
    print(" 所有服务启动中...")
    print("=" * 60)
    print("   • gateway    : http://localhost:8080")
    print("   • user-web   : http://localhost:8000")
    print("   • cv-web     : http://localhost:8001")
    print("   • nlp-web    : http://localhost:8002")
    print("   • favorite   : http://localhost:8003")
    print("   • notice     : http://localhost:8004")
    print("   • cv-worker  : RabbitMQ 消费者")
    print("   • nlp-worker : RabbitMQ 消费者")
    print("=" * 60)
    print("\n 按 Ctrl+C 可停止所有服务\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()