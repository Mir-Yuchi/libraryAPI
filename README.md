# libraryAPI


---

## 📦 Инструкция по запуску

### Клонирование репозитория

```bash
https://github.com/Mir-Yuchi/libraryAPI.git
cd libraryAPI
```

### Установка required packages

```bash
poetry install
```

### Создание и активация виртуального окружения

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### Настройка .env

Скопируйте файл `.env.example` в `.env` и заполните:

```
DATABASE_URL=postgresql://user:pass@host:port/dbname
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Применение миграций

```bash
poetry run alembic upgrade head
```

### Запуск сервера

```bash
uvicorn app.main:app --reload --port 8000
```

### Регистрация первого пользователя

Для создания первого библиотекаря:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"secret"}'
```

---

## 🏗️ Структура проекта

```
libraryAPI/
├── alembic/               # Скрипты миграций Alembic
│   └── versions/
├── app/                   # Логика
│   ├── core/              # Настройки (Pydantic BaseSettings)
│   ├── db/                # SQLAlchemy (engine, session, Base)
│   ├── models/            # ORM-модели
│   ├── schemas/           # Pydantic-схемы
│   ├── crud/              # Функции CRUD и бизнес-логика
│   ├── routers/           # FastAPI-маршруты
│   └── auth/              # JWT, безопасность, зависимости
├── tests/                 # Pytest-тесты (unit и e2e)
├── .env                   # Переменные окружения (игнорируется гитом)
├── pyproject.toml         # Конфигурация Poetry
└── README.md              # Документация на английском
```

---

## 🗄️ Решения по структуре БД

- **users**
    - id (PK), email (unique), password (bcrypt), is_active, created_at.

- **books**
    - id, title, author, year, isbn (unique), copies_available (>=0), description (nullable), created_at.

- **readers**
    - id, name, email (unique), created_at.

- **borrowed_book**
    - id, book_id → FK(books), reader_id → FK(readers), borrow_date, return_date (nullable).

---

## ⚙️ Бизнес-логика

### 4.1 Доступность книги

- Перед выдачей проверяем `copies_available > 0`.
- При выдаче декрементируем `copies_available`.

### 4.2 Лимит для читателя

- Читатель не может иметь более 3 невозвращённых книг одновременно.
- Считаем текущие записи `borrowed_book` с `return_date IS NULL`.

### 4.3 Возврат книги

- Устанавливаем `return_date` на текущее время (UTC).
- Инкрементируем `copies_available`.
- При попытке вернуть несуществующую или уже возвращённую книгу возвращаем ошибку.

**Сложности:**

- Синхронизация `copies_available` при конкурентных запросах решена через транзакции.
- Валидации реализованы на уровне SQLAlchemy и Pydantic v2 для обеспечения целостности данных.

---

## 🔐 Аутентификация

- JWT-токены генерируются с помощью `python-jose` (HS256).
- Хеширование паролей — `passlib[bcrypt]`.
- Проверка токенов через `OAuth2PasswordBearer` в зависимости `get_current_user`.
- Защищены все CRUD-эндпоинты (`/users`, `/books`, `/readers`, `/borrow`), кроме `/auth/*`, чтобы только авторизованные библиотекари могли изменять данные.

---

## ✨ Фича

### Экспорт списка просроченных заимствований в CSV

- Позволяет библиотекарям скачать отчет по всем книгам, срок возврата которых истёк, в формате CSV — без сложных планировщиков и фоновых задач.

**Реализация:**
- Добавить новый endpoint в `app/routers/reports.py`:
```http request
  GET /reports/overdue?format=csv
```
- Внутри обработчика выполнить простой SQL-запрос к таблице `borrowed_book` для выборки записей с `return_date IS NULL` и `borrow_date + INTERVAL 'X days' < NOW().`
- С помощью стандартного модуля csv сформировать строки отчёта (заголовки + данные).
- Вернуть результат через FastAPI `StreamingResponse`, установив заголовок `Content-Disposition: attachment; filename="overdue.csv"` для загрузки файла.
- Клиенту придёт полноценный CSV-файл
