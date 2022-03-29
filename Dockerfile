# syntax=docker/dockerfile:1

FROM python:3.10.2-slim

# do not write pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# do not buffer output
ENV PYTHONUNBUFFERED=1

RUN apt-get update

# create a group and user to run app
ARG APP_USER=somebody
RUN groupadd -r ${APP_USER} && useradd --no-log-init --create-home -r -u 1000 -g ${APP_USER} ${APP_USER}

# create project directory
ARG APP_DIR=/home/${APP_USER}/lx-classroom/
RUN mkdir ${APP_DIR} && chown ${APP_USER}:${APP_USER} ${APP_DIR}

RUN apt-get update && apt-get install -y --no-install-recommends netcat

COPY ./requirements.txt ${APP_DIR}

RUN pip install --no-cache-dir -r ${APP_DIR}requirements.txt

COPY --chown=${APP_USER}:${APP_USER} . ${APP_DIR}

USER ${APP_USER}:${APP_USER}

WORKDIR ${APP_DIR}

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "lx_classroom.wsgi" ]
