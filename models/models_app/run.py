import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "models_app.main:app",
        host="0.0.0.0",
        port=8006,
        reload=True
    )