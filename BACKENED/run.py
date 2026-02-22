import uvicorn
from app.config import settings


def main():
    """
    Entry point to run FastAPI application.
    """

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )


if __name__ == "__main__":
    main()