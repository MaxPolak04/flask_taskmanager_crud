FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

COPY run.py ./

COPY migrations migrations/
RUN mkdir -p migrations/versions

COPY taskmanager_app taskmanager_app/

COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/init_admin.py /init_admin.py

RUN chmod +x /entrypoint.sh

COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh


EXPOSE 8000

ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]
