import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_syndicate.settings')

app = Celery('the_syndicate')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Settings
app.conf.beat_schedule = {
    'regenerate-stats-every-minute': {
        'task': 'game.tasks.regenerate_all_player_stats',
        'schedule': 60.0, # Run every 60 seconds
    },
}