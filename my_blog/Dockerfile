FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV USE_POLLING=True

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000

ENTRYPOINT ["/app/migrate_and_start.sh"]

# docker build -t backend-blog ./my_blog/

# docker run -p 127.0.0.1:8000:8000 --env-file .env -v $(pwd)/my_blog:/app backend-blog
