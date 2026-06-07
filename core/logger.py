import os
import time
import json

LOG_FILE = "data/logs.txt"


def log(action, detail=""):
    data = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "detail": detail
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
