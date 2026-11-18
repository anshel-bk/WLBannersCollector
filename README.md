git clone https://github.com/anshel-bk/WLBannersCollector.git

uv venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Установка пакетов
uv sync


Скопируйте шаблон конфигурации
cp .env.example .env
Откройте .env и заполните реальные значения:

2. Запуск скрипта

uv run main.py

3. Обновление скрипта
сd 'путь к скрипту' git pull