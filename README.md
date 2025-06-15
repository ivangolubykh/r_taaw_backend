# R‑Taaw: Recipes to Remember — Backend

🚧 This project is under active development. Expect breaking changes.

**R‑Taaw** is an open recipe book where users can save recipes, share them, or keep them private.  
This repository contains the **backend** for the project, built with Django.

> ⚠️ Please note: The project name **R-Taaw** and its variants (**D-Taaw**, **C-Taaw**, etc.) are unique identifiers created by **Ivan Golubykh**. Do not use these names in derivative projects or registered trademarks without permission.

> 🧭 The frontend for this project is available at: [https://github.com/ivangolubykh/r_taaw_frontend](https://github.com/ivangolubykh/r_taaw_frontend)

---

## 📦 Tech Stack

- Python 3.13 + Django REST Framework  
- PostgreSQL  
- Docker + Docker Compose  
- JWT Authentication

---

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/ivangolubykh/r_taaw_backend.git
   cd r_taaw_backend
   ```

2. Prepare the environment:
   ```bash
   cp .env.sample .env
   mkdir -p .volumes/db_data .volumes/logs static
   chmod ugo=rwx .volumes/logs
   ```

3. Build and run:
   ```bash
   docker compose build --no-cache
   docker compose up
   ```

4. Initialize the database:
   ```bash
   docker compose exec django_app bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. To stop the containers, run:
   ```bash
   docker compose down
   ```

---

## 📄 Additional Materials

- [`DEVELOPER_GUIDE.md`](DEVELOPER_GUIDE.md) — extended documentation for developers  
- [`TRANSLATION.md`](TRANSLATION.md) — localization instructions  
- [`LICENSE`](LICENSE) — project license (MIT)

---

## 🌐 Project Homepage (planned)

[https://r-taaw.allworld.xyz](https://r-taaw.allworld.xyz)
