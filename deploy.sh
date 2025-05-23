#!/bin/bash

# Автоматический скрипт деплоя для Render.com

# Проверка обязательных переменных
if [ -z "$ADMIN_USER" ] || [ -z "$ADMIN_PASSWORD" ] || [ -z "$PORT" ]; then
  echo "Ошибка: убедитесь, что переменные ADMIN_USER, ADMIN_PASSWORD и PORT заданы."
  exit 1
fi

# 1. Установка зависимостей
echo "🔧 Устанавливаем зависимости..."
pip install -r requirements.txt

# 2. Создание директорий
echo "📂 Создаем системные директории..."
mkdir -p data logs

# 3. Применение миграций БД
echo "🗄️ Инициализируем базу данных..."
flask db upgrade

# 4. Создание администратора (если не существует)
echo "👨💻 Создаем администратора..."
flask create-admin \
    --username "$ADMIN_USER" \
    --password "$ADMIN_PASSWORD"

# 5. Запуск бота и веб-интерфейса
echo "🚀 Запускаем приложение..."
gunicorn --bind 0.0.0.0:"$PORT" \
    --workers 4 \
    --preload \
    --timeout 120 \
    web.web_interface:app &

# Запуск Telegram-бота
python -m app.main
