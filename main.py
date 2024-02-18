from fastapi import FastAPI
from routers import user, photo

app = FastAPI()

app.include_router(user.router)
app.include_router(photo.router)


# Додавання обробника для кореневого URL
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
