FROM python:slim
WORKDIR /code
# ENV FLASK_APP wsgi.py
# ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn --bind 0.0.0.0:$PORT wsgi
# CMD ["flask", "run"]