# docker pull python:3-alpine
# docker build -t kribor/oauth-proxy:latest .
# docker push kribor/oauth-proxy:latest

FROM python:3-alpine

LABEL com.oauth-proxy.version="1.0"

COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt
RUN mkdir /code
COPY flask_oauth_proxy.py /code/
WORKDIR /code

CMD ["python", "./flask_oauth_proxy.py"]
