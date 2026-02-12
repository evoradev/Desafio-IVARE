FROM python:3.14.3

# Evita que o Python crie arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1  

# Logs em tempo real no terminal
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
