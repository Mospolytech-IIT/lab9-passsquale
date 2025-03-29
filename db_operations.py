from models import SessionLocal
from models.models import User, Post


# Функция для добавления пользователей
def add_users():
    with SessionLocal() as session:
        users = [
            User(username="user1", email="user1@example.com", password="123123123"),
            User(username="user2", email="user2@example.com", password="123123123"),
            User(username="user3", email="user3@example.com", password="123123123"),
        ]
        session.add_all(users)
        session.commit()
        print("Пользователи добавлены!")


# Функция для добавления постов
def add_posts():
    with SessionLocal() as session:
        # Получаем пользователей
        users = session.query(User).all()
        posts = [
            Post(title="First Post", content="This is the first post", user_id=users[0].id),
            Post(title="Second Post", content="Hello world!", user_id=users[1].id),
            Post(title="Third Post", content="Learning SQLAlchemy!", user_id=users[0].id),
        ]
        session.add_all(posts)
        session.commit()
        print("Посты добавлены!")


# Функция для извлечения всех пользователей
def get_all_users():
    with SessionLocal() as session:
        users = session.query(User).all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")


# Функция для извлечения всех постов с информацией о пользователях
def get_all_posts_with_users():
    with SessionLocal() as session:
        posts = session.query(Post).all()
        for post in posts:
            user = session.query(User).filter(User.id == post.user_id).first()
            print(f"Post ID: {post.id}, Title: {post.title}, User: {user.username}")


# Функция для извлечения постов конкретного пользователя
def get_posts_by_user(username):
    with SessionLocal() as session:
        user = session.query(User).filter(User.username == username).first()
        if user:
            posts = session.query(Post).filter(Post.user_id == user.id).all()
            for post in posts:
                print(f"Post ID: {post.id}, Title: {post.title}, Content: {post.content}")
        else:
            print("Пользователь не найден!")


# Функция для обновления email пользователя
def update_user_email(username, new_email):
    with SessionLocal() as session:
        user = session.query(User).filter(User.username == username).first()
        if user:
            user.email = new_email
            session.commit()
            print(f"Email пользователя {username} обновлен!")
        else:
            print("Пользователь не найден!")


# Функция для обновления content у поста
def update_post_content(post_id, new_content):
    with SessionLocal() as session:
        post = session.query(Post).filter(Post.id == post_id).first()
        if post:
            post.content = new_content
            session.commit()
            print(f"Содержимое поста ID {post_id} обновлено!")
        else:
            print("Пост не найден!")


# Функция для удаления поста
def delete_post(post_id):
    with SessionLocal() as session:
        post = session.query(Post).filter(Post.id == post_id).first()
        if post:
            session.delete(post)
            session.commit()
            print(f"Пост ID {post_id} удален!")
        else:
            print("Пост не найден!")


# Функция для удаления пользователя и всех его постов
def delete_user_and_posts(username):
    with SessionLocal() as session:
        user = session.query(User).filter(User.username == username).first()
        if user:
            session.query(Post).filter(Post.user_id == user.id).delete()
            session.delete(user)
            session.commit()
            print(f"Пользователь {username} и его посты удалены!")
        else:
            print("Пользователь не найден!")
