# API YaMDb

## Групповой проект по модулю "API: интерфейс взаимодействия программ"

#### Тимлид - Илюшин Павел
#### Участники:
- Илюшин Павел
- Соколов Андрей
- Пескова Александра

## Описание проекта

API YaMDb представляет собой REST API на базе Django Rest Framework. Проект собирает отзывы и комментарии пользователей на произведения искусства (музыка, фильмы, книги), а также предоставляет информацию о рейтинге произведений.

## Технологии

- Python 3.8+
- Django 5.1.1
- Django REST Framework 3.15.2
- SQLite (для разработки)
- JWT аутентификация
- Djoser для управления пользователями

## Установка и запуск

### Предварительные требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)

### Пошаговая инструкция

1. **Клонируйте репозиторий:**
   ```bash
   git clone <url-репозитория>
   cd api-yamdb
   ```

2. **Создайте и активируйте виртуальное окружение:**
   
   Для Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   Для Unix-подобных систем:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Перейдите в директорию с проектом:**
   ```bash
   cd api_yamdb
   ```

5. **Подготовьте и примените миграции:**
   
   Для Windows:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   
   Для Unix-подобных систем:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

6. **Загрузите данные в базу (опционально):**

   Для Windows:
   ```bash
   python manage.py load_csv <имя файла>
   ```
   
   Для Unix-подобных систем:
   ```bash
   python3 manage.py load_csv <имя файла>
   ```

   Файлы данных размещены в директории /static/data/, пример команды:
   ```bash
   python3 manage.py load_csv category.csv
   ```

7. **Запустите проект:**
   
   Для Windows:
   ```bash
   python manage.py runserver
   ```
   
   Для Unix-подобных систем:
   ```bash
   python3 manage.py runserver
   ```

## Документация API

После запуска сервера полная документация проекта доступна по адресу:
**http://127.0.0.1:8000/redoc/**

В документации вы найдете исчерпывающую информацию по:
- Доступным эндпоинтам
- Параметрам запросов
- Примеры ответов API
- Схемы данных

## Структура проекта

```
api_yamdb/
├── api/              # Основное API приложение
├── reviews/          # Приложение для отзывов и комментариев
├── users/            # Приложение для управления пользователями
├── api_yamdb/        # Основные настройки Django
├── static/           # Статические файлы (данные, документация)
├── templates/        # HTML шаблоны
└── manage.py         # Django management script
```

## Тестирование

Для запуска тестов используйте:
```bash
pytest
```

## Лицензия

Этот проект создан в рамках образовательной программы.
