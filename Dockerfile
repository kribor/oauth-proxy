FROM fareoffice/python3

LABEL com.oath-proxy.version="0.2"

COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt

COPY . /code
WORKDIR /code

CMD ["flask_oauth_proxy.py"]