import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket

from auth import authentication
from client import html
from db import models
from db.database import engine
from exceptions import StoryException
from router import articles, blog_get, blog_post, file, product, users
from templates import templates

app = FastAPI()
app.include_router(templates.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(product.router)
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response


@app.get('/hello')
def index():
    return {'message': 'Hello world!'}


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )


@app.get("/")
async def get():
    return HTMLResponse(html)


clients = []


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


models.Base.metadata.create_all(engine)

app.mount('/files', StaticFiles(directory="files"), name='files')

app.mount('/templates/static',
          StaticFiles(directory="templates/static"),
          name="static"
          )
