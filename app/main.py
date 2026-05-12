from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from sqlalchemy import text

#from app.db.config.database import create_db_and_tables
from app.db.config.database import create_db_and_tables
from app.db.config.session import SessionDep
#from app.routers import auth_router
from app.routers import product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Microshop-Products",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    #lifespan=lifespan,
)

#app.include_router(auth_router.router)
app.include_router(product_router.router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "product-service",
    }


@app.get("/ready")
def readiness(session: SessionDep):
    try:
        session.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from None
    return {"status": "ready", "database": "ok"}


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()