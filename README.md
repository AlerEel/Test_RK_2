# Проверки организаций — Автоматизированный парсер и веб-интерфейс

## Описание

Этот проект автоматически собирает данные о проверках организаций с сайта Госуслуг, сохраняет их в базу данных SQLite и предоставляет удобный веб-интерфейс для просмотра с поиском и пагинацией.

**Ключевые особенности:**
- Автоматический парсинг с устойчивостью к ошибкам 504 и временным сбоям
- Повторные попытки с экспоненциальной задержкой
- Автоматическое обновление данных по расписанию через cron
- Веб-интерфейс на Flask + Gunicorn
- Простая диагностика через логи

---

## Быстрый старт (Docker)

1. **Соберите и запустите контейнер:**
   ```sh
   docker-compose up --build
   ```
2. Откройте сайт: [http://localhost:5000](http://localhost:5000)
3. Данные будут автоматически обновляться по расписанию (см. cron).

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
- `parser.py` — извлекает заголовки через Playwright, запускает основной парсер
- `parser_v2.py` — основной парсер API Госуслуг, устойчив к ошибкам, сохраняет данные в БД
- `load_to_sqlite.py` — загрузка данных в SQLite
- `server.py` — Flask-сервер для просмотра данных
- `templates/index.html` — шаблон Bootstrap для веб-интерфейса
- `Dockerfile`, `docker-compose.yml` — автоматизация сборки и запуска
- `requirements.txt` — зависимости Python
- `crontab.txt` — cron-задачи для автоматического обновления данных
- `start.sh` — стартовый скрипт для запуска парсера, сервера и cron

---

## Cron и автоматизация обновления

- Все cron-задачи описаны в `crontab.txt` и копируются в `/etc/cron.d/my-cron` при сборке контейнера.
- Пример содержимого:
  ```
  SHELL=/bin/bash
  PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

  * * * * * root echo "$(date): Cron работает!" >> /var/log/cron.log 2>&1
  */5 * * * * root echo "$(date): [cron] Запускаю parser.py..." >> /var/log/cron.log && cd /app && python parser.py >> /var/log/cron.log 2>&1 && echo "$(date): [cron] parser.py завершён" >> /var/log/cron.log
  @reboot root cd /app && /usr/local/bin/gunicorn -w 2 -t 120 -b 0.0.0.0:5000 server:app >> /var/log/cron.log 2>&1
  ```
- Cron запускается в foreground через `cron -f` в `start.sh`.
- Все логи cron и парсера пишутся в `/var/log/cron.log`.

---

## Диагностика и логи

- Для проверки работы cron используйте:
  ```sh
  tail /var/log/cron.log
  ```
- Строка вида `Cron работает!` должна появляться каждую минуту.
- Для теста cron можно добавить строку с echo в `crontab.txt`.
- Все ошибки и статусы парсера также пишутся в этот лог.

---

## Обработка ошибок

- Парсер автоматически повторяет запросы при ошибках 504, 408, 429, 500, 502, 503, 520-524.
- Используется максимум 5 попыток с экспоненциальной задержкой (1с, 2с, 4с, 8с, 16с).
- Все ошибки и попытки логируются.

---

## Особенности для Windows

- Если вы редактируете cron-файлы или скрипты на Windows, убедитесь, что они в формате LF (Unix), а не CRLF (Windows).
- Для конвертации используйте PowerShell:
  ```powershell
  (Get-Content crontab.txt) | ForEach-Object { $_ -replace "\r", "" } | Set-Content crontab.txt
  (Get-Content start.sh) | ForEach-Object { $_ -replace "\r", "" } | Set-Content start.sh
  ```

---

## База данных

- Используется SQLite (`inspections.db`), создаётся и обновляется автоматически.
- Таблица `inspections` содержит поля: entity_name, ogrn, purpose, status, result, examStartDate.

---

## Порты

- По умолчанию используется порт 5000 (Flask/Gunicorn).
- При запуске через `server.py` — порт 5001.

---

## Пример логов cron
```
Thu Jul 18 10:00:00 MSK 2024: Cron работает!
Thu Jul 18 10:05:00 MSK 2024: [cron] Запускаю parser.py...
Thu Jul 18 10:05:01 MSK 2024: [cron] parser.py завершён
```

---

## Контакты и поддержка

Если у вас возникли вопросы или проблемы с запуском — создайте issue или обратитесь к автору проекта.