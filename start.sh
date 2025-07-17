#!/bin/bash

# Запуск парсинга и загрузки данных при старте
echo "$(date): [start.sh] Выполняю parser.py"
python /app/parser.py && python /app/load_to_sqlite.py

# Запуск Flask-сервера
echo "$(date): [start.sh] Запускаю gunicorn..."
gunicorn -w 2 -t 120 -b 0.0.0.0:5000 server:app &

# Вывод пользовательского сообщения
echo ""
echo "Сервер запущен и доступен по адресу: http://localhost:5000"
echo ""

# Запуск cron (в foreground)
echo "$(date): [start.sh] Запускаю cron..."
cron -f