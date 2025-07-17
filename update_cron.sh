#!/bin/bash
# Добавить cron-задачу для обновления данных каждый час
CRON_FILE=/etc/cron.d/update_data

# Проверяем, что скрипт запущен с правами root
if [ "$EUID" -ne 0 ]; then
    echo "Ошибка: скрипт должен быть запущен с правами root"
    exit 1
fi

# Удаляем старую задачу, если есть
rm -f $CRON_FILE

# Создаем новую cron-задачу
echo "0 * * * * root cd /app && python -u parser.py && python -u load_to_sqlite.py >> /var/log/cron.log 2>&1" > $CRON_FILE

# Устанавливаем правильные права доступа
chmod 0644 $CRON_FILE

# Перезапускаем cron-сервис для применения изменений
if command -v systemctl >/dev/null 2>&1; then
    systemctl restart cron
elif command -v service >/dev/null 2>&1; then
    service cron restart
else
    echo "Предупреждение: не удалось перезапустить cron-сервис"
fi

echo "Cron-задача успешно добавлена: $CRON_FILE"
echo "Задача будет выполняться каждый час в 0 минут"
echo "Логи будут записываться в /var/log/cron.log" 