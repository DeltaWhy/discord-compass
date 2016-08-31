FROM python:3.5
ADD https://github.com/krallin/tini/releases/download/v0.10.0/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
WORKDIR /app
CMD ["python", "-m", "compass"]
