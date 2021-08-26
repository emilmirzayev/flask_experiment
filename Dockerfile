FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN apt-get update -y &&    \
    pip install -r requirements.txt

ENV settings=dev
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
