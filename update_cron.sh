#!/bin/bash
# Добавить cron-задачу для обновления данных каждый час
CRON_FILE=/etc/cron.d/update_data
# Удаляем старую задачу, если есть
rm -f $CRON_FILE
# Логи теперь в /var/log/cron.log

echo "0 * * * * root cd /app && python -u parser.py && python -u load_to_sqlite.py >> /var/log/cron.log 2>&1" > $CRON_FILE
chmod 0644 $CRON_FILE
crontab $CRON_FILE 