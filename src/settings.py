import os
import sys
from git import Repo
import json
import pydantic
import time
import datetime
import re

DEBUG = True
SETTINGS_FOLDER = os.path.abspath(os.path.dirname(__file__))
WORK_FOLDER = os.path.join(SETTINGS_FOLDER, "..")

STORAGE_FOLDER = os.path.join(WORK_FOLDER, "files")
STORAGE_INFORMATION_PATH = os.path.join(STORAGE_FOLDER, "information.json")

REGEX = r"^files\/.*"





