from celery.schedules import crontab
from django.conf import settings

broker_url = settings.CELERY_BROKER_URL
broker_heartbeat = None
broker_connection_timeout = 30  # May require a long timeout due to Linux DNS timeouts etc
event_queue_expires = 60  # Will delete all celeryev. queues without consumers after 1 minute.

include = [
    "background.cron_jobs",
]
accept_content = ["json"]
task_serializer = "json"
result_serializer = "json"
task_time_limit = settings.CELERY_TIME_LIMIT
task_soft_time_limit = settings.CELERY_SOFT_TIME_LIMIT
task_reject_on_worker_lost = True
broker_transport_options = {'max_retries': 10, 'queue_order_strategy': 'priority'}
task_always_eager = settings.CELERY_ALWAYS_EAGER
beat_tz_aware = True
enable_utc = True
timezone = settings.TIME_ZONE
task_queue_max_priority = 10
task_default_priority = 5
task_inherit_parent_priority = True
task_acks_late = True

beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"

task_routes = {
    'background.cron_jobs.update_location_periods': {'queue': 'cron_jobs'},
    'background.cron_jobs.check_grid_point_change': {'queue': 'cron_jobs'},
    'background.cron_jobs.schedule_location_periods': {'queue': 'cron_jobs'},
    'background.cron_jobs.schedule_location_grid_point': {'queue': 'cron_jobs'},
}

beat_schedule = {
    'schedule_location_periods': {
        'task': 'background.cron_jobs.schedule_location_periods',
        'schedule': crontab(minute="*/30"),
        'args': (),
    },
    'schedule_location_grid_point': {
        'task': 'background.cron_jobs.schedule_location_grid_point',
        'schedule': crontab(hour="0", minute="15"),
        'args': (),
    },
}
