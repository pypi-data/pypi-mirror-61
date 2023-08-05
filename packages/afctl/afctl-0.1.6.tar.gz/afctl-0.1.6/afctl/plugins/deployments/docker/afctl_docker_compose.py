from mako.template import Template

def docker_compose_template(path):
    template = Template(

"""
version: '2.1'
services:
  redis:
    image: 'redis:5.0.5'
    # command: redis-server --requirepass redispass

  postgres:
    image: postgres:9.6
    environment:
      - POSTGRES_USER=airflow
      - POSTGRES_PASSWORD=airflow
      - POSTGRES_DB=airflow
    # Uncomment these lines to persist data on the local filesystem.
    #     - PGDATA=/var/lib/postgresql/data/pgdata
    # volumes:
    #     - ./pgdata:/var/lib/postgresql/data/pgdata

  webserver:
    image: puckel/docker-airflow:1.10.6
    restart: always
    depends_on:
      - postgres
      - redis
    environment:
      - LOAD_EX=n
      - FERNET_KEY=46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=
      - EXECUTOR=Celery
      # - POSTGRES_USER=airflow
      # - POSTGRES_PASSWORD=airflow
      # - POSTGRES_DB=airflow
      # - REDIS_PASSWORD=redispass
    volumes:
      - ../${path}/dags:/usr/local/airflow/dags
      # Uncomment to include custom plugins
      # - ../plugins:/usr/local/airflow/plugins
    ports:
      - "8080:8080"
    command: webserver
    healthcheck:
      test: ["CMD-SHELL", "[ -f /usr/local/airflow/airflow-webserver.pid ]"]
      interval: 30s
      timeout: 30s
      retries: 3

  flower:
    image: puckel/docker-airflow:1.10.6
    restart: always
    depends_on:
      - redis
    environment:
      - EXECUTOR=Celery
      # - REDIS_PASSWORD=redispass
    ports:
      - "5555:5555"
    command: flower

  scheduler:
    image: puckel/docker-airflow:1.10.6
    restart: always
    depends_on:
      - webserver
    volumes:
      - ../${path}/dags:/usr/local/airflow/dags
      # Uncomment to include custom plugins
      # - ../plugins:/usr/local/airflow/plugins
    environment:
      - LOAD_EX=n
      - FERNET_KEY=46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=
      - EXECUTOR=Celery
      # - POSTGRES_USER=airflow
      # - POSTGRES_PASSWORD=airflow
      # - POSTGRES_DB=airflow
      # - REDIS_PASSWORD=redispass
    command: scheduler

  worker:
    image: puckel/docker-airflow:1.10.6
    restart: always
    depends_on:
      - scheduler
    volumes:
      - ../${path}/dags:/usr/local/airflow/dags
      # Uncomment to include custom plugins
      # - ../plugins:/usr/local/airflow/plugins
    environment:
      - FERNET_KEY=46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=
      - EXECUTOR=Celery
      # - POSTGRES_USER=airflow
      # - POSTGRES_PASSWORD=airflow
      # - POSTGRES_DB=airflow
      # - REDIS_PASSWORD=redispass
    command: worker
"""
    )

    return template.render_unicode(path=path)