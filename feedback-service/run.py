import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "feedback_app.main:app",
        host="0.0.0.0",
        port=8008,
        reload=True
    )