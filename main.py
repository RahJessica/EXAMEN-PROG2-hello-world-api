import datetime
from typing import List

from fastapi import FastAPI, requests
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse, HTMLResponse
from fastapi import Header
from fastapi import Response

app = FastAPI()

# Q1
@app.get("/ping", status_code=status.HTTP_200_OK)
def read_hello():
    return {"Pong"}

#Q2
@app.get("/home", status_code=status.HTTP_200_OK)
def welcome_home():
    return HTMLResponse (
        """
            <!doctype html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>None</title>
                </head>
                <body>
                    <h1>Welcome home!</h1>
                </body>
            </html>
        """
    )

#Q4
class Post (BaseModel):
    author: str
    title: str
    content: str

posts_db: List[Post] = [
    Post(
        author="Lucas Clavel",
        title="Les temps d'automne",
        content="Livre long"
    )
]

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_posts (post: List[Post]):
    posts_db.extend(post)
    return posts_db

#Q5
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts ():
    return posts_db

#Q6
@app.put("/posts", status_code=status.HTTP_200_OK)
def put_posts (new_post: Post):
    for i, existing_post in enumerate(posts_db):
        if existing_post.Number == new_post.title:
            if existing_post != new_post:
                posts_db[i] = new_post
                return {"message": "Post mis à jour", "post": new_post}
            else:
                return {"message": "Aucune modification, post identique", "post": new_post}

    posts_db.append(new_post)
    return {"message": "Nouveau post ajouté", "post": new_post}