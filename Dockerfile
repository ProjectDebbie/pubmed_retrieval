FROM python:3.7.5-slim
WORKDIR /usr/src/app

RUN pip3 install biopython
RUN pip3 install argparse

COPY pubmed_timed_retrieval.py .

CMD [ "python", "pubmed_timed_retrieval.py" ]
