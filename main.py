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
    
    """
    The custom_middleware function is a middleware function that adds the time it took to process the request in seconds
    to the response headers. This can be used for performance monitoring.
    
    :param request: Request: Get the request object
    :param call_next: Call the next middleware in the chain
    :return: A response object with a header named 'performance'
    :doc-author: Trelent
    """
    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers['performance'] = str(during)
    return response


templates = Jinja2Templates(directory='templates')

# Додавання обробника для кореневого URL
@app.get("/", response_class=HTMLResponse, description="Main page")
async def root(request: Request):
    
    """
    The root function is the entry point for all requests to the server.
    It returns a response object that contains an HTML page with a greeting.
    
    :param request: Request: Get the request object from the client
    :return: A response object that contains the html of our index
    :doc-author: Trelent
    """
    return templates.TemplateResponse('index.html', {"request": request, "title": "Instagram Арр"})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    
    """
    The healthchecker function is used to check the health of the database.
        It will return a 200 status code if it can successfully connect to the database,
        and a 500 status code otherwise.
    
    :param db: Session: Pass the database session to the function
    :return: A dictionary with a message
    :doc-author: Trelent
    """
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
    
    """
    The show_qr_code function takes a photo_id as an argument and returns the QR code associated with that photo.
        If no such QR code exists, it raises a 404 error.
    
    :param photo_id: int: Get the photo id from the url
    :param request: Request: Pass the request object to the template
    :param db: Session: Access the database
    :return: A templateresponse object
    :doc-author: Trelent
    """
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
