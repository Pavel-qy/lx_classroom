from celery import shared_task
from datetime import datetime
import time
from lx_classroom import celery_app

# tasks using @shared_task decorator
# @shared_task
# def write_some_message_task(msg, *args):
#     time.sleep(1)
#     with open("celery-worker.txt", "a") as file:
#         file.write(f"\n{msg} on {datetime.utcnow()}:\n{args}\n")


# @shared_task
# def write_some_message_task_prior(msg, *args):
#     time.sleep(2)
#     with open("celery-worker-prior.txt", "a") as file:
#         file.write(f"\n{msg} on {datetime.utcnow()}:\n{args}\n")


# class based tasks
class WriteSomeMessageTask(celery_app.Task):
    def run(self, msg, *args):
        time.sleep(1)
        with open("celery-worker.txt", "a") as file:
            file.write(f"\n{msg} on {datetime.utcnow()}:\n{args}\n")

WriteSomeMessageTask = celery_app.register_task(WriteSomeMessageTask())


class WriteSomeMessageTaskPrior(celery_app.Task):
    def run(self, msg, *args):
        time.sleep(2)
        with open("celery-worker-prior.txt", "a") as file:
            file.write(f"\n{msg} on {datetime.utcnow()}:\n{args}\n")

WriteSomeMessageTaskPrior = celery_app.register_task(WriteSomeMessageTaskPrior())
