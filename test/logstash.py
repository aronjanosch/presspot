import logstash
import json
import re
import ndjson
import os


path = 'test/logs/cleaned'
files = os.listdir(path)
files = [f for f in files if os.path.isfile(path+'/'+f)]
# https://regex101.com/r/6SVdaz/1
m = re.compile('(INFO) (.{23}) \[\'(\d*.\d*.\d*.\d*)\'\] (\w*) (http:\/\/(.+?(?=\/)).+?) content:(\'.*\') headers:(\{.*\})')

for old_file in files:
    file = open((os.path.join(path, old_file)), 'r')
    print(old_file)
    log_list = []

    while True:

        line = file.readline()
        if not line:
            break
        g = m.search(line)
        if g:
            try: 
                log_list.append({
                    '@timestamp':g.group(2),
                    'ip':g.group(3),
                    'request.IP':g.group(3),
                    'request.headers.X-Forwarded-For':g.group(3),
                    'request.method':g.group(4),
                    'request.host':g.group(6),
                    'request.url':g.group(5),
                    'request.content':g.group(7),
                    #'request.headers':g.group(8)
                })
                
                # log_list.append({
                #     '@timestamp':g.group(2),
                #     'request':{
                #         'IP':g.group(3),
                #         'content':g.group(7),
                #         'headers':{
                #             'X-Forwarded-For':g.group(3)
                #         },
                #         'host':g.group(6),
                #         'method':g.group(4),
                #         'url':g.group(5)
                #     }
                # })
            except Exception as e:
                print(e)
                print(line)

    with open((os.path.join((path + "/ndjson"), old_file)) + '.ndjson', 'w') as outfile:
        ndjson.dump(log_list, outfile)

print('DONE')
#print(json.dumps(log_list, indent=4))