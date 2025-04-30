FROM --platform=linux/amd64 python:3.9-slim-buster

ENV SECRET_KEY="S3cRetK3y"

WORKDIR /app

COPY . /app

RUN mv /app/flag.txt /Fl4g_is_H3r3.txt

RUN pip install flask

EXPOSE 5000

CMD ["python", "/app/app.py"]