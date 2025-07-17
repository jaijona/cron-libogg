# strip_data/cron_task.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strip_data.settings')
django.setup()

from cron_strip.utils import guardar_promedios_stripchat

guardar_promedios_stripchat()