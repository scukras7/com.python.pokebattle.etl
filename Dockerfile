FROM python:3.9.12

ARG SCRIPT_DIR=/opt/python

RUN mkdir -p ${SCRIPT_DIR}

COPY data/ ${SCRIPT_DIR}/data/
COPY etl/ ${SCRIPT_DIR}/etl/
COPY services/ ${SCRIPT_DIR}/services/
COPY requirements.txt ${SCRIPT_DIR}/

RUN cd ${SCRIPT_DIR} && \
    pip install -r requirements.txt

WORKDIR ${SCRIPT_DIR}/etl
