from fastapi import FastAPI
from app.routers import auth, users, bulk, reports, yopass

app = FastAPI(
    title="FreeIPA API",
    description="API для управления пользователями FreeIPA",
    version="1.0.0"
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users - CRUD"])
app.include_router(bulk.router, tags=["Users - Bulk"])
app.include_router(reports.router, tags=["Analytics"])
app.include_router(yopass.router, tags=["Yopass"])