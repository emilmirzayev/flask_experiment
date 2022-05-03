FROM python:3.9
WORKDIR /app 
COPY . .
RUN apt-get update -y &&    \ 
    pip install -r requirements.txt --user
 
ENV settings=dev 
EXPOSE 5000

RUN ["chmod", "+x", "./entrypoint.sh"]
ENTRYPOINT ["bash", "entrypoint.sh"]
CMD gunicorn -c gunicorn_conf.py server:app