import os
from celery import Celery
from celery.schedules import crontab
from datetime import datetime

# from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lx_classroom.settings')

app = Celery('lx_classroom')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# schedule task for celerybeat. write message every 10 sec
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test_writer.s('hello'), name='add every 10')

#     # # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(30.0, test.s('world'), expires=10)

#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=15, minute=52, day_of_week='tuesday'),
#         test_writer.s('Happy Tuesdays!'),
#     )

@app.task
def test_writer(arg):
    with open("test_writer.txt", "a") as file:
        file.write(f"{arg} at {datetime.now()}\n")
