FROM python:3.6

LABEL language="python"
LABEL framework="flask"
LABEL usage="kmeans"

RUN apt-get update

ADD kmeans /usr/local/kmeans
RUN cd /usr/local/kmeans && pip3 install -r requirements.txt && python3 setup.py install

ADD wsgi.py /usr/local/bin/wsgi.py
RUN chmod +x /usr/local/bin/wsgi.py

RUN mkdir /var/local/kmeans /var/local/kmeans/logs
ADD logging.conf /var/local/kmeans

EXPOSE 5000

ENV FLASK_ENV="production" FLASK_DEBUG="false" 
ENV TLS_CERTIFICATE="" TLS_KEY=""

WORKDIR /var/local/kmeans
CMD ["/usr/local/bin/wsgi.py"]
