import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "notice_app.main:app",
        host="0.0.0.0",
        port=8005,
        reload=True
    )