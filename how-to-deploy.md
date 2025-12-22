# 0. Freeze packages
make freeze

# 1. Generate SSL certificates
make certs

# 2. Start all containers (Gunicorn + Nginx)
make up

# 3. Create superuser
make superuser

# 4. Follow logs
make logs

# 5. Update zero-downtime
make update
