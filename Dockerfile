# Stage 1: Build stage
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      curl \
      nodejs \
      npm && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies in a separate directory (avoid installing in /usr/local)
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/install/lib/python3.11/site-packages"

# Copy your source code
COPY . .

# Build your Tailwind CSS assets
WORKDIR /app/etl_project/theme/static_src
RUN npm install

WORKDIR /app/etl_project
RUN python manage.py tailwind install
RUN python manage.py tailwind build

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Stage 2: Final lightweight image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

WORKDIR /app/etl_project

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

EXPOSE 8087

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "etl_project.wsgi:application", "--bind", "0.0.0.0:8087", "--timeout", "90"]