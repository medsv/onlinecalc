# Используем официальный образ Python 3.12 (slim-версия для меньшего размера)
FROM python:3.12-slim

# Метаданные образа
LABEL maintainer="engpython@yandex.ru"
LABEL description="Инженерные расчёты онлайн (калькуляторы)"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только requirements.txt (чтобы кэшировать установку зависимостей)
COPY requirements.txt .

# Устанавливаем системные зависимости для SciPy и очищаем кэш
RUN apt-get update && apt-get install -y libblas3 liblapack3 && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir -r requirements.txt

# Копируем только нужные папки (сначала редко изменяемые)
COPY common/ ./common/
COPY libs/ ./libs/
COPY img/ ./img/
COPY main.py ./
COPY pages/ ./pages/

# Открываем порт Streamlit
EXPOSE 8080

# Создаем конфигурационный файл Streamlit
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "
[server]
headless = true
port = 8080
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
" > /root/.streamlit/config.toml'

# Запускаем приложение
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]

# Исправлены ошибки синтаксиса в RUN командах