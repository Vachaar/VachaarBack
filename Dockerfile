FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
ENV PYTHONUNBUFFERED 1

EXPOSE 80

CMD ["sh", "-c", "python manage.py migrate"]