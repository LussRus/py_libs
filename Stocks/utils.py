from inspect import currentframe
from pathlib import Path
import json

class DEBUG:
    def __init__(self, mode=True):
        self.debug = mode

    def debug(self, msg):
        if self.debug:
            cf = currentframe()
            print(f"[#{cf.f_back.f_lineno}] {msg}")

# There are the routines for an array of dicts
class JSON_DB:
    def __init__(self, filename):
        self.filename = filename
        my_file = Path(filename)
        if not my_file.is_file():
            try:
                with open(filename, 'w') as f:
                    a = []
                    json.dump(a, f)
            except Exception as err:
                print(f"Can't create file: {filename}. Error: {err}")

    def put(self, dict):
        with open(self.filename, 'r') as f:
            arr = json.load(f)
            if dict not in arr:
                arr.append(dict)
                with open(self.filename, 'w') as fw:
                    json.dump(arr, fw)

    def list(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def delete(self, key, val):
        with open(self.filename, 'r') as f:
            arr = json.load(f)

            res = []
            for el in arr:
                if el[key] != val:
                    res.append(el)
            with open(self.filename, 'w') as fw:
                json.dump(res, fw)
            return f"Deleted {len(arr) - len(res)}"

    def update(self, key, val, new_dict, insert=True):
        with open(self.filename, 'r') as f:
            arr = json.load(f)
            upd_count = 0
            res = []
            for el in arr:
                if el[key] == val:
                    res.append(new_dict)
                    upd_count += 1
            if upd_count == 0 and insert:
                res.append(new_dict)
            with open(self.filename, 'w') as fw:
                json.dump(res, fw)
            return f"Deleted {len(arr) - len(res)}"