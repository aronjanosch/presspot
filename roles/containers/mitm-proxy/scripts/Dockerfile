FROM python:3

RUN pip3 install mitmproxy
RUN pip3 install python-logstash

RUN mkdir -p /scripts

CMD /usr/local/bin/mitmdump --showhost --listen-host=0.0.0.0 --listen-port=8080 --set block_global=false --ssl-insecure -s /scripts/reverseproxy.py