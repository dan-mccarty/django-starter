#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

prompt() {
  local label="$1"
  local default_value="$2"
  local input

  if [ -n "$default_value" ]; then
    printf "%s [%s]: " "$label" "$default_value"
  else
    printf "%s: " "$label"
  fi

  IFS= read -r input
  if [ -z "$input" ]; then
    input="$default_value"
  fi

  printf "%s" "$input"
}

get_env_value() {
  local file_path="$1"
  local key="$2"

  if [ ! -f "$file_path" ]; then
    return 0
  fi

  awk -F= -v k="$key" 'BEGIN{v=""} $0 ~ "^"k"=" {v=substr($0, index($0, "=")+1)} END{print v}' "$file_path"
}

replace_literal() {
  local file_path="$1"
  local old="$2"
  local new="$3"

  if [ ! -f "$file_path" ]; then
    return 0
  fi

  python3 - "$file_path" "$old" "$new" <<'PY'
import io
import sys
from pathlib import Path

path = Path(sys.argv[1])
old = sys.argv[2]
new = sys.argv[3]

data = path.read_text(encoding="utf-8")
path.write_text(data.replace(old, new), encoding="utf-8")
PY
}

set_env_key() {
  local file_path="$1"
  local key="$2"
  local value="$3"

  if [ ! -f "$file_path" ]; then
    return 0
  fi

  python3 - "$file_path" "$key" "$value" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
key = sys.argv[2]
value = sys.argv[3]

lines = path.read_text(encoding="utf-8").splitlines()
updated = False
for i, line in enumerate(lines):
    if line.startswith(f"{key}="):
        lines[i] = f"{key}={value}"
        updated = True
        break

if not updated:
    lines.append(f"{key}={value}")

path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
}

set_nginx_server_name() {
  local file_path="$1"
  local server_name_value="$2"

  if [ ! -f "$file_path" ]; then
    return 0
  fi

  python3 - "$file_path" "$server_name_value" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
value = sys.argv[2]

lines = path.read_text(encoding="utf-8").splitlines()
for i, line in enumerate(lines):
    stripped = line.lstrip()
    if stripped.startswith("server_name "):
        indent = line[: len(line) - len(stripped)]
        lines[i] = f"{indent}server_name {value};"

path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
}

nginx_conf="$ROOT_DIR/nginx/nginx.conf"
base_env="$ROOT_DIR/.env"
prod_env="$ROOT_DIR/.env.prod"

current_project_name=$(awk -F= '/^PROJECT_NAME=/{print $2; exit}' "$ROOT_DIR/infrastructure/deploy.sh")
current_app_user=$(awk -F= '/^APP_USER=/{print $2; exit}' "$ROOT_DIR/infrastructure/bootstrap.sh")
current_server_name=$(awk '/server_name/{print $2; exit}' "$nginx_conf" | tr -d ';')

current_allowed_hosts_dev=$(get_env_value "$base_env" "ALLOWED_HOSTS")
current_allowed_hosts_prod=$(get_env_value "$prod_env" "ALLOWED_HOSTS")
current_csrf_dev=$(get_env_value "$base_env" "CSRF_TRUSTED_ORIGINS")
current_csrf_prod=$(get_env_value "$prod_env" "CSRF_TRUSTED_ORIGINS")
current_domain_dev=$(get_env_value "$base_env" "DOMAIN")
current_domain_prod=$(get_env_value "$prod_env" "DOMAIN")

project_name=$(prompt "Project name (used in /home/<user>/<project>)" "$current_project_name")
app_user=$(prompt "Deploy user" "$current_app_user")
server_name=$(prompt "Nginx server_name (space-separated)" "$current_server_name")

allowed_hosts_dev=$(prompt "ALLOWED_HOSTS for .env (comma-separated)" "$current_allowed_hosts_dev")
allowed_hosts_prod=$(prompt "ALLOWED_HOSTS for .env.prod (comma-separated)" "$current_allowed_hosts_prod")
csrf_dev=$(prompt "CSRF_TRUSTED_ORIGINS for .env (comma-separated)" "$current_csrf_dev")
csrf_prod=$(prompt "CSRF_TRUSTED_ORIGINS for .env.prod (comma-separated)" "$current_csrf_prod")
domain_dev=$(prompt "DOMAIN for .env" "$current_domain_dev")
domain_prod=$(prompt "DOMAIN for .env.prod" "$current_domain_prod")

# Update infra files for project/user
for file in \
  "$ROOT_DIR/infrastructure/deploy.sh" \
  "$ROOT_DIR/infrastructure/bootstrap.sh" \
  "$ROOT_DIR/infrastructure/hooks.json" \
  "$ROOT_DIR/infrastructure/systemd/github-webhook.service" \
  "$ROOT_DIR/generate_certs.sh"; do
  replace_literal "$file" "$current_project_name" "$project_name"
  replace_literal "$file" "$current_app_user" "$app_user"
  replace_literal "$file" "/home/$current_app_user/$current_project_name" "/home/$app_user/$project_name"
  replace_literal "$file" "/home/$current_app_user" "/home/$app_user"
  replace_literal "$file" "PROJECT_NAME=$current_project_name" "PROJECT_NAME=$project_name"
  replace_literal "$file" "APP_USER=$current_app_user" "APP_USER=$app_user"
done

# Update nginx server_name
set_nginx_server_name "$nginx_conf" "$server_name"

# Update env files
set_env_key "$base_env" "ALLOWED_HOSTS" "$allowed_hosts_dev"
set_env_key "$prod_env" "ALLOWED_HOSTS" "$allowed_hosts_prod"
set_env_key "$base_env" "CSRF_TRUSTED_ORIGINS" "$csrf_dev"
set_env_key "$prod_env" "CSRF_TRUSTED_ORIGINS" "$csrf_prod"
set_env_key "$base_env" "DOMAIN" "$domain_dev"
set_env_key "$prod_env" "DOMAIN" "$domain_prod"

printf "\n✅ Updated project configuration.\n"
