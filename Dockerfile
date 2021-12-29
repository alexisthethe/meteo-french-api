FROM python:3.8.12-alpine3.15

WORKDIR /root/app

COPY requirements.txt /root/app/requirements.txt

RUN pip install -r requirements.txt

COPY app.py /root/app/app.py
COPY run.sh /root/app/run.sh
COPY meteofrenchapi /root/app/meteofrenchapi

CMD [ "/bin/sh", "run.sh" ]
