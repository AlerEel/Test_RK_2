#!/bin/bash
# Скрипт для проверки состояния cron в контейнере

echo "=== Проверка состояния cron ==="

# Проверяем, запущен ли cron
if pgrep cron > /dev/null; then
    echo "✓ Cron-сервис запущен"
else
    echo "✗ Cron-сервис НЕ запущен"
fi

# Проверяем файл с задачами
CRON_FILE=/etc/cron.d/update_data
if [ -f "$CRON_FILE" ]; then
    echo "✓ Файл cron-задач найден: $CRON_FILE"
    echo "Содержимое файла:"
    cat "$CRON_FILE"
else
    echo "✗ Файл cron-задач НЕ найден: $CRON_FILE"
fi

# Проверяем логи cron
if [ -f "/var/log/cron.log" ]; then
    echo "✓ Файл логов найден: /var/log/cron.log"
    echo "Последние 10 строк логов:"
    tail -10 /var/log/cron.log
else
    echo "✗ Файл логов НЕ найден: /var/log/cron.log"
fi

# Проверяем системные логи cron
echo "Последние записи в системных логах cron:"
grep cron /var/log/syslog 2>/dev/null | tail -5 || echo "Системные логи cron недоступны"

echo "=== Проверка завершена ===" 