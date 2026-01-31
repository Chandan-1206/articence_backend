import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Server running!")
    print("👉 Open: http://127.0.0.1:8000/health")
    print("👉 Docs: http://127.0.0.1:8000/docs\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
