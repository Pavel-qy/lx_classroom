import os
import queue
import time
from celery import Celery
from celery.schedules import crontab
from datetime import datetime
from kombu import Exchange, Queue

# from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lx_classroom.settings')

app = Celery('lx_classroom')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# celery queues

# first attempt -- doesn't work.
# app.conf.update({
#     'task_routes': {
#         'lx_classroom.celery.count_registered_users_periodic_task': {'queue': 'periodic_tasks'},
#         'api.tasks.write_some_message_task': {'queue': 'users_registration'}
#     },
#     'task_serializer': 'json',
#     'result_serializer': 'json',
#     'accept_content': ['json']
# })


# second attempt on the pattern from the documentation -- works
app.conf.task_routes = {
    'lx_classroom.celery.count_registered_users_periodic_task': {
        'queue': 'periodic_tasks',
        'routing_key': 'periodic_tasks',
        'priority': 0,
        },
    # tasks implemented by function
    # 'api.tasks.write_some_message_task': {
    #     'queue': 'users_registration',
    #     'routing_key': 'users_registration',
    #     'priority': 9,
    #     },
    # 'api.tasks.write_some_message_task_prior': {
    #     'queue': 'users_registration',
    #     'routing_key': 'users_registration',
    #     'priority': 0,
    #     },
    # class-based tasks
    'api.tasks.WriteSomeMessageTask': {
        'queue': 'users_registration',
        'routing_key': 'users_registration',
        'priority': 9,
        },
    'api.tasks.WriteSomeMessageTaskPrior': {
        'queue': 'users_registration',
        'routing_key': 'users_registration',
        'priority': 0,
        },
    }


# third attempt based on article "5 tips for writing... Doesn't work as expected"
# _ALLOWED_QUEUES = ('periodic_tasks', 'users_registration')
# app.conf.task_create_missing_queues = False
# app.conf.task_queues = tuple(
#     Queue(name=q, exchange=Exchange(q), routing_key=q) for q in _ALLOWED_QUEUES
#     )

# fourth attempt. Creation queues manually
# default_exchange = Exchange("default", type='direct')

# default_queue = Queue(
#     "defautl",
#     default_exchange,
#     routing_key="default"
# )

# periodic_tasks = Queue(
#     "periodic_tasks",
#     default_exchange,
#     routing_key="periodic_tasks"
# )

# users_registration = Queue(
#     "users_registration",
#     default_exchange,
#     routing_key="users_registration"
# )

# app.conf.task_queues = (default_queue, periodic_tasks, users_registration)

# app.conf.task_default_queue = 'default' 
# app.conf.task_default_exchange = 'default'
# app.conf.task_default_routing_key = 'default'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# schedule task for celerybeat. write message every 10 sec
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(
        100.0, 
        count_registered_users_periodic_task.s(), 
        name='add every 100',
        # queue='periodic_tasks'
        )

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=15, minute=52, day_of_week='tuesday'),
    #     test_writer.s('Happy Tuesdays!'),
    # )

@app.task
def count_registered_users_periodic_task():
    try:
        with open("celery-worker.txt", "r") as file:
            row_count = len(file.read().split("\n\n"))
    except FileNotFoundError:
        row_count = 0
    try:
        with open("registered-users-counter.txt", "r") as file:
            last_users_number = int(file.readlines()[-1].split()[-1])
    except FileNotFoundError:
        last_users_number = 0
    time.sleep(5)
    if last_users_number != row_count:
        with open("registered-users-counter.txt", "a") as file:
            file.write(f"Number of registered users on {datetime.utcnow()}: {row_count}\n")
