import json

test_data = json.load(open('test_data.json', 'r'))


def clean_lists(dict):
    for k, v in dict.items():
        if isinstance(v, list) and len(v) < 2:
            dict[k] = v[0]


clean_lists(test_data["_source"]["request"]["headers"])

print(json.dumps(test_data, indent=4))

