# Dockerfile
FROM python:3.7-slim
WORKDIR /blog
RUN git clone https://github.com/pavkozlov/blog_server /blog \
    && pip install -r /blog/requirements.txt
CMD python manage.py migrate && gunicorn --bind 0.0.0.0:8000 server.wsgi