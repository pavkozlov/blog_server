# Dockerfile
FROM python:3.7.5
WORKDIR /blog
RUN git clone https://github.com/pavkozlov/blog_server /blog \
    && pip install -r /blog/requirements.txt \
    && python manage.py migrate
CMD gunicorn --bind 0.0.0.0:8000 server.wsgi