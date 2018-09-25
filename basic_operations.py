import time
import json


def which_watch(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print()
        print(func.__name__, 'took', time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))
        print()
        return result
    return wrapper


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def dump_utf_json(entries, json_file):
    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, sort_keys=True, indent=2)
