FROM apache/superset:latest

USER root

RUN /bin/bash -c "source /app/.venv/bin/activate && pip install psycopg2-binary"

COPY ./superset_entrypoint.sh /app/superset_home/superset_entrypoint.sh

RUN chmod +x /app/superset_home/superset_entrypoint.sh

USER superset

ENTRYPOINT ["/app/superset_home/superset_entrypoint.sh"]
