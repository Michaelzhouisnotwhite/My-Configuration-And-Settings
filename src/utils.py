import os
import settings
import json

def print_when_debug(*args, **kwargs):
    if settings.DEBUG:
        print(*args, **kwargs)


def read_json_file(path: str, mode="r"):
    with open(path, mode, encoding="utf-8") as f:
        res: dict = json.load(f)
    return res


def write_json_file(data: dict, path: str, mode="w"):
    with open(path, mode, encoding="utf-8") as f:
        json.dump(data, f, indent=2)
