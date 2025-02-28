from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Field, Session, select
from db import init_db, get_session
from models import Post, PostBase, PostUpdate
from contextlib import asynccontextmanager
from datetime import datetime


app = FastAPI()



@app.get('/posts/')
async def get_posts(session: Session= Depends(get_session)) -> list[Post]:
    posts = session.exec(select(Post)).all()
    return posts

@app.get('/posts/{post_id}/')
async def get_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        return HTTPException(status_code=404, details="Post is not found")
    return post

@app.post('/posts/')
async def create_post(post_data: PostBase, session: Session = Depends(get_session)) -> Post:
    post = Post(title=post_data.title, content=post_data.content)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@app.delete('/posts/{post_id}/')
async def delete_post(post_id: int, session: Session = Depends(get_session)) -> str:
    post = session.get(Post, post_id)
    if not post:
        return HTTPException(status_code=404)

    session.delete(post)
    session.commit()
    return "Post deleted successfully"



@app.put('/posts/{post_id}/')
async def update_post(post_id: int, post_data: PostUpdate, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content

    session.add(post)
    session.commit()
    session.refresh(post)
    
    return {"message": "Post updated successfully"}