FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-setuptools

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .env .

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app", "--reload"]

