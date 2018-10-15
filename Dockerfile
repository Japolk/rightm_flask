FROM python:3.6

RUN useradd rightm_flask

WORKDIR /home/rightm_flask

COPY requirements.txt requirements.txt
COPY boot.sh boot.sh
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY api api
RUN chmod +x boot.sh

ENV FLASK_APP api
RUN chown -R rightm_flask:rightm_flask ./
USER rightm_flask

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
