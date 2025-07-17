FROM python:3.11-slim

WORKDIR /app

# Установим системные зависимости для playwright и cron
RUN apt-get update && \
    apt-get install -y curl cron tzdata && \
    rm -rf /var/lib/apt/lists/*

# Установим часовой пояс Europe/Moscow (UTC+3)
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" > /etc/timezone

# Установим зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установим браузеры для playwright
RUN python -m playwright install --with-deps

# Копируем проект
COPY . .

# Копируем cron-скрипты и делаем их исполняемыми
COPY update_cron.sh /update_cron.sh
COPY check_cron.sh /check_cron.sh
RUN chmod +x /update_cron.sh /check_cron.sh

# Открываем порт для Flask
EXPOSE 5000

# Запуск: сначала обновление данных, настройка cron, потом запуск cron и gunicorn
CMD ["/bin/bash", "-c", "python -u parser.py && python -u load_to_sqlite.py && /update_cron.sh && echo 'Сайт: http://localhost:5000' && touch /var/log/cron.log && cron -f & gunicorn -w 2 -t 120 -b 0.0.0.0:5000 server:app"] 