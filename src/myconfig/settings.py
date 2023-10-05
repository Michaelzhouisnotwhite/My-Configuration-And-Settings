import os
import sys
from enum import Enum


class Platform(Enum):
    WINDOWS = "windows"
    LINUX = "linux"


if sys.platform.system().lower() == 'windows':
    CUR_PLATFORM = Platform.WINDOWS
elif sys.platform.system().lower() == 'linux':
    CUR_PLATFORM = Platform.LINUX
else:
    raise RuntimeError("current system platform not supported")


_DEV = True
SETTING_DIR = os.path.abspath(os.path.dirname(__file__))
if _DEV:
    CONFIG_FILE_DIR = os.path.join(SETTING_DIR, "../../config")

else:
    if CUR_PLATFORM == Platform.WINDOWS:
        user_profile_path = os.getenv("USERPROFILE")
    elif CUR_PLATFORM == Platform.LINUX:
        user_profile_path = os.getenv("HOME")
        
    CONFIG_FILE_DIR = os.path.join(user_profile_path, ".my-config")
