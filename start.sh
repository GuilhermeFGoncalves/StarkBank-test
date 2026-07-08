#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    echo "Creating virtualenv..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt

if [ -f .env ]; then
    set -a
    source .env
    set +a
else
    echo "Warning: .env not found (copy .env.example and fill it in)." >&2
fi

python manage.py migrate

celery -A config worker --loglevel=info &
celery -A config beat --loglevel=info &
trap 'kill $(jobs -p) 2>/dev/null' EXIT

exec python manage.py runserver "${1:-0.0.0.0:8000}"
