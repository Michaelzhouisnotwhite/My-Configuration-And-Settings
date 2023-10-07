from datetime import datetime
import os

import pytz
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


def check_cache_folder() -> bool:
    if not os.path.exists(settings.CACHE_DIR):
        os.makedirs(settings.CACHE_DIR)
    return True


def get_cur_time() -> str:
    return datetime.now(pytz.timezone(settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")

def str2timestamp(date_time_string: str):
    return datetime.strptime(date_time_string, "%Y-%m-%d %H:%M:%S")