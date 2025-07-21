from app import get_app_prod
from app.config import settings

app = get_app_prod()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.backend.port, log_level="info")
