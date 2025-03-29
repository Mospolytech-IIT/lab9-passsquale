from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models import engine, Base, SessionLocal
from models.models import User, Post

# Создание приложения FastAPI
app = FastAPI()

# Настройка шаблонов Jinja2
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Создание базы данных при старте
Base.metadata.create_all(bind=engine)


# Зависимость для создания сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Главная страница
@app.get("/")
def read_root():
    return RedirectResponse(url="/users")


# Список всех пользователей
@app.get("/users")
def list_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


# Форма для создания нового пользователя
@app.get("/users/new")
def new_user_form(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request})


# Обработка создания нового пользователя
@app.post("/users/new")
def create_user(
        username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    return RedirectResponse(url="/users", status_code=303)


# Страница редактирования пользователя
@app.get("/users/edit/{user_id}")
def edit_user_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_edit_form.html", {"request": request, "user": user})


# Обработка обновления пользователя
@app.post("/users/edit/{user_id}")
def update_user(user_id: int, username: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.email = email
    db.commit()
    return RedirectResponse(url="/users", status_code=303)


# Удаление пользователя
@app.get("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(Post).filter(Post.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return RedirectResponse(url="/users", status_code=303)


# Список всех постов
@app.get("/posts")
def list_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})


# Форма для создания нового поста
@app.get("/posts/new")
def new_post_form(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("post_form.html", {"request": request, "users": users})


# Обработка создания нового поста
@app.post("/posts/new")
def create_post(
        title: str = Form(...), content: str = Form(...), user_id: int = Form(...), db: Session = Depends(get_db)
):
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    return RedirectResponse(url="/posts", status_code=303)


# Страница редактирования поста
@app.get("/posts/edit/{post_id}")
def edit_post_form(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    users = db.query(User).all()
    return templates.TemplateResponse("post_edit_form.html", {"request": request, "post": post, "users": users})


# Обработка обновления поста
@app.post("/posts/edit/{post_id}")
def update_post(post_id: int, title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = title
    post.content = content
    db.commit()
    return RedirectResponse(url="/posts", status_code=303)


# Удаление поста
@app.get("/posts/delete/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return RedirectResponse(url="/posts", status_code=303)
