FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y procps openssl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY django/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY django/ /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Start Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--pid", "/tmp/gunicorn.pid"]
