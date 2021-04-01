FROM python:3.8-slim
ARG VERSION

RUN apt-get update \
    && apt-get install -y --no-install-recommends sqlite python3-pip

ENV VERSION="${VERSION}"
ENV PYTHON_VERSION="3.8"
ENV PYTHONPATH="/usr/local/lib/python${PYTHON_VERSION}/site-packages"

RUN groupadd flask \
    && useradd -m -d /var/local/clustering_outliers -g flask flask

RUN pip3 install --upgrade pip
COPY requirements.txt requirements-testing.txt ./
RUN pip3 install --prefix=/usr/local -r requirements.txt -r requirements-testing.txt

ENV FLASK_APP="clustering_outliers" \
    FLASK_ENV="testing" \
    FLASK_DEBUG="false" \
    OUTPUT_DIR="./output" \
    SHAPE_ENCODING="utf-8"

COPY run-nosetests.sh /
RUN chmod a+x /run-nosetests.sh
ENTRYPOINT ["/run-nosetests.sh"]