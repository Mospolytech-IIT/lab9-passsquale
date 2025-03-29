from models import Base, engine
from db_operations import (
    add_users, add_posts, get_all_users, get_all_posts_with_users,
    get_posts_by_user, update_user_email, update_post_content,
    delete_post, delete_user_and_posts
)


# Создание таблиц
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы!")


if __name__ == "__main__":
    # Шаг 1: Создаем таблицы
    create_tables()

    # Шаг 2: Добавляем данные
    print("\nДобавление пользователей:")
    add_users()

    print("\nДобавление постов:")
    add_posts()

    # Шаг 3: Извлечение данных
    print("\nВсе пользователи:")
    get_all_users()

    print("\nВсе посты с информацией о пользователях:")
    get_all_posts_with_users()

    print("\nПосты пользователя 'john_doe':")
    get_posts_by_user("john_doe")

    # Шаг 4: Обновление данных
    print("\nОбновление email пользователя 'john_doe':")
    update_user_email("john_doe", "new_email@example.com")
    get_all_users()

    print("\nОбновление содержимого поста ID 1:")
    update_post_content(1, "Updated content for the first post")
    get_all_posts_with_users()

    # Шаг 5: Удаление данных
    print("\nУдаление поста ID 2:")
    delete_post(2)
    get_all_posts_with_users()

    print("\nУдаление пользователя 'jane_doe' и всех его постов:")
    delete_user_and_posts("jane_doe")
    get_all_users()
    get_all_posts_with_users()
