import urequests as requests
import uos, machine

def fetch_remote_version(url):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print("OTA check error:", e)
    return None

def read_local_version():
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except:
        return "0.0.0"

def update_if_needed(remote_json):
    local = read_local_version()
    remote = remote_json.get("version")
    if remote > local:
        print("Updating from", local, "to", remote)
        try:
            new_code = requests.get(remote_json["url"])
            if new_code.status_code == 200:
                with open("main.py", "w") as f:
                    f.write(new_code.text)
                with open("version.txt", "w") as vf:
                    vf.write(remote)
                print("Update complete! Rebooting.")
                machine.reset()
        except Exception as e:
            print("Update failed:", e)
