from fastapi import FastAPI
from routers import user, photo, auth

app = FastAPI()

app.include_router(user.router)
app.include_router(photo.router)
app.include_router(auth.router) #18/02/2024 Olha


# Додавання обробника для кореневого URL
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
