from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routers import users, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
