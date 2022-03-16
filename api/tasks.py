from celery import shared_task
from datetime import datetime
import os


@shared_task
def add(a, b):
    print("\n***ADD METHOD***\n")
    return a + b


@shared_task
def write_some_message(filename, *args):
    print(f"{os.getcwd()=}")
    with open(f"{filename}", "a") as file:
        file.write(f"\n Recieved data on {datetime.utcnow()}:\n{args}\n")
