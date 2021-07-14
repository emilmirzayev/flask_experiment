FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN apt-get update -y &&    \
    pip install -r requirements.txt && \
    apt-get install -y postgresql-client

ENV settings=dev
EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]