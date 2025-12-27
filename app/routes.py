from fastapi import FastAPI
from app.routers import auth, users, bulk, reports, yopass

def setup_routes(app: FastAPI) -> None:
    app.include_router(auth.router, tags=["Authentication"])
    app.include_router(users.router, tags=["Users - CRUD"])
    app.include_router(bulk.router, tags=["Users - Bulk"])
    app.include_router(reports.router, tags=["Analytics"])
    app.include_router(yopass.router, tags=["Yopass"])