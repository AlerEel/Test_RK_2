FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y bash && \
    apt-get install -y dos2unix && \
    apt-get clean && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

# Установка часового пояса
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    echo "Europe/Moscow" > /etc/timezone

# Копируем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Установка playwright браузеров
RUN python -m playwright install --with-deps

# Копируем crontab и настраиваем
COPY crontab.txt /etc/cron.d/my-cron
RUN chmod 0644 /etc/cron.d/my-cron

RUN touch /var/log/cron.log && chmod a+rw /var/log/cron.log

# Копируем и делаем исполняемым стартовый скрипт
COPY start.sh /start.sh
RUN dos2unix /start.sh && \
    chmod +x /start.sh
    
# Открытие порта для Flask
EXPOSE 5000

# Запуск стартового скрипта
CMD ["/start.sh"]
