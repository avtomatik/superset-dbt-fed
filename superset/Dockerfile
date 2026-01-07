FROM apache/superset:latest

USER root

RUN pip install --no-cache-dir psycopg2-binary

RUN pip install --no-cache-dir "psycopg[binary]"

COPY ./superset_entrypoint.sh /app/superset_home/superset_entrypoint.sh

RUN chmod +x /app/superset_home/superset_entrypoint.sh

USER superset

ENTRYPOINT ["/app/superset_home/superset_entrypoint.sh"]
