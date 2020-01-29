# Dockerfile

FROM python:latest

WORKDIR /blog
# Copy project
COPY . /blog/
RUN pip install -r /blog/requirements.txt

CMD gunicorn --bind 0.0.0.0:8000 server.wsgi