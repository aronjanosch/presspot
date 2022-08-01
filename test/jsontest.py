import json

container_json = json.load(open('wordpress_containers.json', 'r'))

for i in container_json:
    print(i['url'])