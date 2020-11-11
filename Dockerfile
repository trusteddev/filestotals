FROM python:3.6-alpine

RUN adduser -D filestotals

WORKDIR /home/filestotals

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY filestotals.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP filestotals.py

RUN chown -R filestotals:filestotals ./
USER filestotals

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
