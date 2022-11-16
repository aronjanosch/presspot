# Script to prepare logs for the inport in elastic search
import base64
import logstash
import json
import re
import ndjson
import os

# Path of the logs that are ment to be cleaned
path = 'test/logs/cleaned'
files = os.listdir(path)
files = [f for f in files if os.path.isfile(path+'/'+f)]
# RegEx to detect parts of the logs
m = re.compile('(INFO) (.{23}) \[\'(\d*.\d*.\d*.\d*)\'\] (\w*) (http:\/\/(.+?(?=\/)).+?) content:(\'.*\') headers:(\{.*\})')

log_list = []

# Iterate over all files in the directory
for old_file in files:
    file = open((os.path.join(path, old_file)), 'r')
    print(old_file)
    
    # Operations on every line within the file
    while True:

        line = file.readline()
        if not line:
            break
        
        # Search with RegEx
        g = m.search(line)
        if g:
            try: 
                # Create an python dictionary that is the base for ndjson
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

            except Exception as e:
                print(e)
                print(line)

# Write all log entries from all log files into a single ndjson file
with open((os.path.join((path + "/ndjson"), 'full_logfile')) + '.ndjson', 'w') as outfile:
    ndjson.dump(log_list, outfile)

print('DONE')