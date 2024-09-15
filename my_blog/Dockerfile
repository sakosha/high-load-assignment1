# hlb_assignment1
FROM python:3.11.10-slim-bookworm


WORKDIR /app

COPY requirements.txt /app/
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]
RUN ["rm", "requirements.txt"]

COPY . /app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
