import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "forum_app.main:app",
        host="0.0.0.0",
        port=8007,
        reload=True
    )