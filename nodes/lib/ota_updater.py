import requests
import json
import os
import sys

def fetch_remote_version(url):
    try:
        r = requests.get(url)
        if r.ok:
            return r.json()
    except Exception as e:
        print(f"OTA version check error: {e}")
    return None

def read_local_version():
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except:
        return "0.0.0"

def update_if_needed(remote):
    local = read_local_version()
    remote_version = remote.get("version", "0.0.0")
    if remote_version > local:
        print(f"Updating from {local} → {remote_version}")
        try:
            r = requests.get(remote["url"])
            if r.ok:
                with open("main.py", "w") as f:
                    f.write(r.text)
                with open("version.txt", "w") as vf:
                    vf.write(remote_version)
                print("Update complete. Restarting.")
                os.execv(sys.executable, ['python3'] + sys.argv)
        except Exception as e:
            print(f"OTA update failed: {e}")
