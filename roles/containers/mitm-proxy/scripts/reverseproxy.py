from mitmproxy import http, ctx
import logging
import os

Request_Log = {}
Log_Format = "%(levelname)s %(asctime)s - %(message)s"

log_path = "/scripts/logfile.log"
abs_log_path = os.path.abspath(log_path)

logging.basicConfig(filename = log_path,
                    filemode = "w",
                    format = Log_Format,
                    level = logging.INFO
)

logger = logging.getLogger()

def b64_or_str(d):
    if isinstance(d, str):
        encoded = d
    else:
        encoded = codecs.encode(d, "base64").decode().strip()

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

def req2dict(request):
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
        'content': resp.content,
        'cookies': resp.cookies,
        'headers': resp.headers
    }


def request(flow: http.HTTPFlow) -> None:
    # pretty_host takes the "Host" header of the request into account,
    # which is useful in transparent mode where we usually only have the IP
    # otherwise.
    if flow.request.pretty_host == "press.wordpress.0rn.de":
        flow.request.host = "wordpress"

def response(flow: http.HTTPFlow) -> None:

    if not flow.id in Request_Log:
        Request_Log[flow.id] = {
            'request': req2dict(flow.request),
            'response': resp2dict(flow.response)
        }
    
    request = req2dict(flow.request)

    firstline = str(request['headers']['X-Real-IP']) + " - " + str(request['method']) + ": " + str(request['url']) + "| content: " + str(request['content'])
    secondline = str(request['cookies'])
    logger.info(firstline + "\n" + secondline)
    
    
    