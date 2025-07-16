# Проверки организаций — Автоматизированный парсер и веб-интерфейс

## Описание

Этот проект автоматически собирает данные о проверках организаций с сайта Госуслуг, сохраняет их в базу данных SQLite и предоставляет удобный веб-интерфейс для просмотра с поиском и пагинацией.

---

## Быстрый старт в Docker

1. **Соберите и запустите контейнер:**
   ```sh
   docker-compose up --build
   ```
2. Откройте сайт: [http://localhost:5000](http://localhost:5000)
3. Данные будут автоматически обновляться каждый час (cron внутри контейнера).

---

## Запуск без Docker (локально)

1. Установите Python 3.11+ и зависимости:
   ```sh
   pip install -r requirements.txt
   python -m playwright install --with-deps
   ```
2. Запустите парсер и загрузку данных:
   ```sh
   python parser.py
   ```
3. Запустите сервер:
   ```sh
   python server.py
   ```
4. Откройте сайт: [http://localhost:5000](http://localhost:5000)

---

## Структура проекта
- `parser.py` — основной запуск парсинга (Playwright), передаёт заголовки в парсер API.
- `parser_v2.py` — парсер API Госуслуг, сразу загружает данные в БД.
- `load_to_sqlite.py` — функции для загрузки данных в SQLite (без работы с JSON).
- `server.py` — Flask-сервер для просмотра данных.
- `templates/index.html` — внешний вид сайта (Bootstrap, карточки).
- `Dockerfile`, `docker-compose.yml`, `update_cron.sh` — для автоматизации и запуска в Docker.
- `requirements.txt` — зависимости Python.

---

## Возможные ошибки

 - Есть вероятность, что при скачивании проект на ПК(windows) update_cron.sh будет сохранен в формате CRLF (Windows)
 - Вам нужно перевести его в LF (Unix-формат)
 - Для это переходим в powershell(Вводим "powershell" в адресную строку проводника, находясь в папке с проектом)
 - Вводим команду:
      (Get-Content update_cron.sh) | ForEach-Object { $_ -replace "\r", "" } | Set-Content update_cron.sh
 - Готово, собираем контейнер