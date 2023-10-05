import os
import sys
from git import Repo
import json
import pydantic
import time
import datetime
import re
TIMEZONE = 'Asia/Shanghai'
DEBUG = True
SETTINGS_FOLDER = os.path.abspath(os.path.dirname(__file__))
WORK_FOLDER = os.path.join(SETTINGS_FOLDER, "..")

STORAGE_FOLDER = os.path.join(WORK_FOLDER, "files")
STORAGE_INFORMATION_PATH = os.path.join(STORAGE_FOLDER, "information.json")

TOKEN_PATH = os.path.join(WORK_FOLDER, ".token")
GIST_ID = "ce932a0803ee4e84e255a191f6726e2c"
REGEX = r"^files\/.*"
