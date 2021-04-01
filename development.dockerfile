FROM python:3.8-slim
ARG VERSION

LABEL language="python"
LABEL framework="flask"
LABEL usage="Clustering and outlier detection service for rasters and vectors"

RUN apt-get update \
    && apt-get install -y --no-install-recommends sqlite python3-pip

ENV VERSION="${VERSION}"
ENV PYTHON_VERSION="3.8"
ENV PYTHONPATH="/usr/local/lib/python${PYTHON_VERSION}/site-packages"

RUN groupadd flask \
    && useradd -m -d /var/local/clustering_outliers -g flask flask

RUN pip3 install --upgrade pip

RUN mkdir /usr/local/clustering_outliers/
COPY setup.py requirements.txt requirements-production.txt /usr/local/clustering_outliers/
COPY clustering_outliers /usr/local/clustering_outliers/clustering_outliers

RUN cd /usr/local/clustering_outliers \
    && pip3 install --prefix=/usr/local -r requirements.txt -r requirements-production.txt \
    && python setup.py install --prefix=/usr/local

COPY wsgi.py docker-command.sh /usr/local/bin/
RUN chmod a+x /usr/local/bin/wsgi.py /usr/local/bin/docker-command.sh

WORKDIR /var/local/clustering_outliers
RUN mkdir ./logs && chown flask:flask ./logs
COPY --chown=flask logging.conf .

ENV FLASK_APP="clustering_outliers" \
    FLASK_ENV="production" \
    FLASK_DEBUG="false" \
    INSTANCE_PATH="/var/local/clustering_outliers/data" \
    TEMPDIR="" \
    SECRET_KEY_FILE="/var/local/clustering_outliers/secret_key" \
    TLS_CERTIFICATE="" \
    TLS_KEY=""

USER flask
CMD ["/usr/local/bin/docker-command.sh"]

EXPOSE 5000
EXPOSE 5443