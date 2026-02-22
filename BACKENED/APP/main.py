from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import time

from app.config import settings
from app.database import connect_to_database, close_database_connection, check_database_health
from app.utils.logger import get_logger

# Routers
from app.routers import (
    auth,
    patients,
    doctors,
    appointments,
    billing,
    prescriptions,
    ai_routes,
)

# ==========================================
# 🚀 INITIALIZE APP
# ==========================================

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

logger = get_logger("main")


# ==========================================
# 🌐 CORS MIDDLEWARE
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)


# ==========================================
# 🔌 DATABASE STARTUP & SHUTDOWN
# ==========================================

@app.on_event("startup")
async def startup():
    logger.info(" Starting application...")
    connect_to_database()


@app.on_event("shutdown")
async def shutdown():
    logger.info(" Shutting down application...")
    close_database_connection()


# ==========================================
# 📡 REQUEST LOGGING MIDDLEWARE
# ==========================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Incoming request: {request.method} {request.url}")

    response = await call_next(request)

    process_time = round(time.time() - start_time, 4)
    logger.info(f"Completed {request.method} {request.url} "
                f"Status: {response.status_code} "
                f"Time: {process_time}s")

    return response


# ==========================================
# ❌ GLOBAL EXCEPTION HANDLER
# ==========================================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": exc.errors()},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"},
    )


# ==========================================
# 📦 INCLUDE ROUTERS
# ==========================================

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(billing.router)
app.include_router(prescriptions.router)
app.include_router(ai_routes.router)


# ==========================================
# ❤️ HEALTH CHECK
# ==========================================

@app.get("/health", tags=["Health"])
async def health_check():
    db_status = check_database_health()
    return {
        "status": "healthy" if db_status else "database_unavailable",
        "database": db_status,
        "environment": settings.ENVIRONMENT,
    }


# ==========================================
# 🏠 ROOT ENDPOINT
# ==========================================

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Hospital Management System with GenAI is running 🚀",
        "version": settings.APP_VERSION,
    }