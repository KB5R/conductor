from fastapi import FastAPI

app = FastAPI(
    title="FreeIPA API",
    description="API для управления пользователями FreeIPA",
    version="1.0.0"
)