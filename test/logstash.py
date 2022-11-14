import logstash
import json
import re
import ndjson

log_list = []
file = 'logfile_19-07.log'
# https://regex101.com/r/qO7aKv/1
m = re.compile('(INFO) (.{23}) - \[\'(\d*.\d*.\d*.\d*)\'] - (\w*): (http:\/\/.+?(?=\/))(.+?(?=\|))\| content: (.*)')

with open(file) as f:
    lines = f.readlines()
    for line in lines:
        if line[0] == "{":
            continue
        g = m.search(line)
        if g:
            log_list.append({
                '@timestamp':g.group(2),
                'request.IP':g.group(3),
                'request.headers.X-Forwarded-For':g.group(3),
                'request.method':g.group(4),
                'request.headers.Host':g.group(5),
                'request.path':g.group(6),
                'request.content':g.group(7)
            }
            )

with open('logfile.ndjson', 'w') as outfile:
    ndjson.dump(log_list, outfile)

print('DONE')
#print(json.dumps(log_list, indent=4))