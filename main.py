from fastapi import FastAPI
from routers import user, photo

app = FastAPI()

app.include_router(user.router)
app.include_router(photo.router)