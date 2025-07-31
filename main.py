import json
from fastapi import FastAPI, Request
from starlette.responses import Response, JSONResponse
from typing import List
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


@app.get("/ping")
def ping():
    return Response(content="pong", media_type="text/plain", status_code=200)

@app.get("/home")
def home():
    html_content = "<h1>Welcome home!</h1>"
    return Response(content=html_content, media_type="text/html", status_code=200)

@app.get("/{full_path:path}")
def error():
    not_found_html = "<p>404 NOT FOUND</p>" 
    return Response(content=not_found_html, media_type="text/html", status_code=404)

class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

posts = []

@app.post("/posts")
def add_posts(new_posts: List[Post]):
    posts.extend(new_posts)
    return JSONResponse(content=[post.model_dump(mode="json") for post in posts], status_code=201)

@app.get("/posts")
def get_posts():
    if not posts:
        return JSONResponse(content={"message": "No posts found"}, status_code=404)
    return JSONResponse(content=[post.model_dump(mode="json") for post in posts], status_code=200)