
FROM python:3.8


WORKDIR /app


COPY . /app

ENV FLASK_APP=main.py

RUN pip install -r requirements.txt


CMD ["flask", "run", "--host=0.0.0.0"]
