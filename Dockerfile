FROM python:3.7.5-slim
WORKDIR /usr/src/app

RUN pip install biopython
RUN pip install argparse

COPY pubmed_timed_retrieval .

CMD [ "python", "pubmed_timed_retrieval.py" ]