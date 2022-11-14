from mitmproxy import http, ctx
from mitmproxy.net.http.cookies import CookieAttrs
import logstash
import logging
import os
import datetime
import codecs
import json
import base64

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logfilename = datetime.datetime.now().strftime('mylogfile_%H_%M_%d_%m_%Y.log')
log_path = "/scripts/{filename}".format(filename = str(logfilename))
abs_log_path = os.path.abspath(log_path)

logging.basicConfig(filename = log_path,
                    filemode = "w",
                    format = Log_Format,
                    level = logging.INFO
)

logger = logging.getLogger()


json_logger = logging.getLogger('presspot')
json_logger.setLevel(logging.INFO)
logstash_host = 'logstash'
json_logger.addHandler(logstash.TCPLogstashHandler(logstash_host, 5959 , version=1))


container_json = json.load(open('/scripts/wordpress_containers.json', 'r'))

def isBase64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False

def b64_or_str(d):
    if isinstance(d, str):
        encoded = d
    else:
        encoded = (base64.b64decode(d.decode().strip())).decode().strip()

    return encoded

def multi2dict(multi):
    data = {}
    for k,v in multi.items(multi=True):
        if not k in data:
            data[k] = []
        # Cookie handling
        if isinstance(v, tuple) and len(v) >= 2:
            if isinstance(v[1], CookieAttrs):
                v = [v[0]]
            elif isinstance(v[2], CookieAttrs):
                v = [v[0], v[1]]
        if isinstance(v, list):
            v = list(map(lambda x: b64_or_str(x), v))
        else:
            v = [b64_or_str(v)]
        data[k] += v

    return data

def clean_lists(dict):
    for k, v in dict.items():
        if isinstance(v, list) and len(v) < 2:
            dict[k] = v[0]
    return dict

def req2dict(request):
    data = {
        'scheme': request.scheme,
        'host': request.host,
        'method': request.method,
        'port': request.port,
        'path': request.path,
        'content': b64_or_str(request.content),
        'url': request.url,
        'cookies': multi2dict(request.cookies),
        'query': multi2dict(request.query),
        'headers':clean_lists(multi2dict(request.headers)),
        'multipart_form': multi2dict(request.multipart_form)
    }
    return data

def req2dict_old(request):
    data = {
        'scheme': request.scheme,
        'host': request.host,
        'method': request.method,
        'port': request.port,
        'path': request.path,
        'content': request.content,
        'url': request.url,
        'cookies': multi2dict(request.cookies),
        'query': multi2dict(request.query),
        'headers':multi2dict(request.headers),
        'multipart_form': multi2dict(request.multipart_form)
    }
    return data



def resp2dict(resp):
    return {
        'status_code': resp.status_code,
        #'content': resp.content,
        'cookies': multi2dict(resp.cookies),
        #'headers': multi2dict(resp.headers)
    }


def request(flow: http.HTTPFlow) -> None:
#     # pretty_host takes the "Host" header of the request into account,
#     # which is useful in transparent mode where we usually only have the IP
#     # otherwise.

    for item in container_json:
        if flow.request.pretty_host == item['url']:
            flow.request.host = item['hostname']
            flow.request.host_header = item['url']

    if flow.request.pretty_host == "press.wordpress.0rn.de":
        flow.request.host = "wordpress"
        flow.request.host_header = "press.wordpress.0rn.de"
#     else:
#         flow.request.host = "wordpress"
        
    


def response(flow: http.HTTPFlow) -> None:

    req_log = {
        'request': req2dict(flow.request),
        'response': resp2dict(flow.response)
        }
    req_log['request']['IP'] = req_log['request']['headers']['X-Real-IP']
    
    ctx.log.info(req_log['request']['content'])


    request = req2dict_old(flow.request)
    
    json_logger.info('INFO', extra = req_log)

    firstline = str(request['headers']['X-Real-IP']) + " - " + str(request['method']) + ": " + str(request['url']) + "| content: " + str(request['content'])
    secondline = str(request['cookies'])
    logger.info(firstline + "\n" + secondline)
    