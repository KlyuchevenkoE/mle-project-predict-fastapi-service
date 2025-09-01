set -e

SCRIPT_DIR=$(dirname "$0")
ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "Ошибка: .env не найден по пути $ENV_FILE" >&2
  exit 1
fi

set -a
. "$ENV_FILE"
set +a

exec mlflow server \
  --backend-store-uri "postgresql://${DB_DESTINATION_USER}:${DB_DESTINATION_PASSWORD}@${DB_DESTINATION_HOST}:${DB_DESTINATION_PORT}/${DB_DESTINATION_NAME}?sslmode=require&target_session_attrs=read-write" \
  --default-artifact-root "s3://${S3_BUCKET_NAME}/" \
  --no-serve-artifacts \
  --host 0.0.0.0 \
  --port "${MLFLOW_PORT:-5000}"