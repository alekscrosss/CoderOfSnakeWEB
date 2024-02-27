# file main.py

import time
from fastapi import Request
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.responses import HTMLResponse
from src.db.database import get_db
from src.db.models import ImageLink
from fastapi.templating import Jinja2Templates


from src.routes import auth, photo, comments, tags, image_links

app = FastAPI()

@app.middleware('http')
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers['performance'] = str(during)
    return response


templates = Jinja2Templates(directory='templates')

# Додавання обробника для кореневого URL
@app.get("/", response_class=HTMLResponse, description="Main page")
async def root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "title": "Instagram Арр"})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
    #Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

@app.get("/show-qr/{photo_id}")
async def show_qr_code(photo_id: int, request: Request, db: Session = Depends(get_db)):
    image_link = db.query(ImageLink).filter(ImageLink.photo_id == photo_id).first()
    if image_link is None:
        raise HTTPException(status_code=404, detail="Image link not found")
    qr_code_data = image_link.qr_code
    return templates.TemplateResponse("qr_code_page.html", {"request": request, "qr_code_data": qr_code_data})

app.include_router(auth.router, prefix='/api')
app.include_router(photo.router, prefix='/api', tags=['photo'])
app.include_router(comments.router, prefix='/api', tags=['comments'])
app.include_router(tags.router, prefix='/api', tags=['tags'])
app.include_router(image_links.router, prefix='/api', tags=['QR-code'])
