#!/usr/bin/env bash
set -e

cron
rm twistd.pid || echo "ignore"

cd web_ui
python3 manage.py collectstatic --noinput
python3 manage.py migrate

# Create admin account if not exists
cat <<EOF | python3 manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()  # get the currently active user model,
User.objects.filter(username='admin').exists() or \
    User.objects.create_superuser('admin', 'admin@demo.com', 'admin')
EOF

cd ..
honcho start