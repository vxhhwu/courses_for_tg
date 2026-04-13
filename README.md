# courses_for_tg
Eng:
# 📚 Online Courses Telegram Bot

A full-featured Telegram bot for an online course platform. Users can register, browse courses by category, enroll, track their courses in a personal account, and cancel enrollment. Administrators can add, view, and delete courses.

## ✨ Features

- **User registration** – first name, last name, age (FSM, duplicate check)
- **Course catalog** – categories (Biology, Maths, Russian, Chemistry, Programming)
- **Dynamic course lists** – courses are fetched from the database for each category
- **Course details** – title, description, price, enrollment button
- **Enrollment system** – prevents double enrollment
- **Personal account** – view profile, list of enrolled courses, cancel enrollment
- **Profile deletion** – removes user data (cascade deletion of enrollments)
- **Admin panel** – add course (FSM), view all courses, delete course by ID
- **Error handling** – missing courses, unregistered users, empty categories

## 🛠️ Tech Stack

- Python 3.11+
- aiogram 3.x (FSM, routers, callback queries)
- aiosqlite (asynchronous SQLite)
- SQLite (three databases: users, courses, enrollments)

## 🚀 Installation

1. Clone the repository  
   `git clone https://github.com/yourusername/online-courses-bot.git`
2. Create virtual environment  
   `python -m venv venv`
3. Activate it  
   - Windows: `venv\Scripts\activate`  
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies  
   `pip install aiogram python-dotenv aiosqlite`
5. Create `.env` file with your bot token  
   `TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
6. Run the bot  
   `python run.py`

## 📁 Project Structure

## 🤖 Bot Commands

### User commands
- `/start` – welcome message and main menu
- `/reg` – register (if not registered)
- `/cancel` – cancel current FSM operation

### Admin commands (only for predefined user ID)
- `/adm_sc` – add new course (FSM steps: id, title, description, category, price)
- `/adm_gc` – show all courses
- `/adm_dc <course_id>` – delete course by ID

## 🗄️ Database Schema

### `database_users.db`
- `users` (user_id INTEGER PRIMARY KEY, first_name, last_name, age, registered_at)

### `database_courses.db`
- `courses` (id INTEGER PRIMARY KEY, title, description, category, price, created_at)

### `database_mycourses.db`
- `my_courses` (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id, course_id, title, description, category, price, enrolled_at, UNIQUE(user_id, course_id))

## 📝 Notes

- The admin user ID is hardcoded in `handlers.py` (1385387997). Change it to your own Telegram ID.
- Categories in the catalog correspond to the `category` field in the `courses` table (biology, maths, russian, chemistry, programming).
- When a user deletes their profile, all their enrollments are also deleted (cascade).

Rus:
# 📚 Telegram-бот «Платформа онлайн‑курсов»

Полнофункциональный бот для образовательной платформы. Пользователи могут регистрироваться, просматривать курсы по категориям, записываться на курсы, отслеживать их в личном кабинете и отписываться. Администраторы могут добавлять, просматривать и удалять курсы.

## ✨ Возможности

- **Регистрация пользователя** – имя, фамилия, возраст (FSM, проверка дубликатов)
- **Каталог курсов** – категории (Биология, Математика, Русский язык, Химия, Программирование)
- **Динамический вывод курсов** – курсы подгружаются из БД для каждой категории
- **Детальная карточка курса** – название, описание, цена, кнопка «Записаться»
- **Запись на курс** – защита от повторной записи
- **Личный кабинет** – просмотр профиля, список записанных курсов, отписка
- **Удаление профиля** – каскадное удаление записей на курсы
- **Админ‑панель** – добавление курса (FSM), просмотр всех курсов, удаление курса по ID
- **Обработка ошибок** – отсутствие курсов, незарегистрированные пользователи, пустые категории

## 🛠️ Технологии

- Python 3.11+
- aiogram 3.x (FSM, роутеры, callback‑кнопки)
- aiosqlite (асинхронная работа с SQLite)
- SQLite (три базы данных: пользователи, курсы, записи)

## 🚀 Установка

1. Клонируйте репозиторий  
   `git clone https://github.com/yourusername/online-courses-bot.git`
2. Создайте виртуальное окружение  
   `python -m venv venv`
3. Активируйте его  
   - Windows: `venv\Scripts\activate`  
   - Linux/Mac: `source venv/bin/activate`
4. Установите зависимости  
   `pip install aiogram python-dotenv aiosqlite`
5. Создайте файл `.env` с токеном бота  
   `TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
6. Запустите бота  
   `python run.py`

## 📁 Структура проекта

## 🤖 Команды бота

### Пользовательские команды
- `/start` – приветствие и главное меню
- `/reg` – регистрация (если не зарегистрирован)
- `/cancel` – отмена текущей операции FSM

### Административные команды (только для заданного ID)
- `/adm_sc` – добавить новый курс (FSM: id, название, описание, категория, цена)
- `/adm_gc` – показать все курсы
- `/adm_dc <id_курса>` – удалить курс по ID

## 🗄️ Схема базы данных

### `database_users.db`
- `users` (user_id INTEGER PRIMARY KEY, first_name, last_name, age, registered_at)

### `database_courses.db`
- `courses` (id INTEGER PRIMARY KEY, title, description, category, price, created_at)

### `database_mycourses.db`
- `my_courses` (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id, course_id, title, description, category, price, enrolled_at, UNIQUE(user_id, course_id))

## 📝 Примечания

- ID администратора захардкожен в `handlers.py` (1385387997). Замените на свой Telegram ID.
- Категории в каталоге соответствуют полю `category` в таблице `courses` (biology, maths, russian, chemistry, programming).
- При удалении профиля пользователя все его записи на курсы также удаляются (каскад).
