FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=development
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=""
ENV DJANGO_SUPERUSER_EMAIL=admin@admin.com
ENV PORT 8000
EXPOSE 8000

WORKDIR /app
RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && \
    pipenv requirements --exclude-markers > requirements.txt && \
    pip install -r /tmp/requirements.txt
COPY . /app

RUN chmod +x /app/docker-entrypoint.sh && \
    groupadd -g 1024 django && \
    useradd --no-log-init -u 1024 -g 1024 django && \
    chown django:django -R /app

USER 1024

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
