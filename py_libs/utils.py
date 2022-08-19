import re
from inspect import currentframe
import os, datetime
from dateutil import parser


class roll_arr:
    def __init__(self, size):
        self.size = size
        self.arr = []

    def push(self, el):
        self.arr.append(el)
        if len(self.arr) > self.size:
            self.arr.pop(0)

    def member(self, el):
        if el in self.arr:
            return True
        return False

class DEBUG:
    def __init__(self, mode=True):
        self.debug = mode

    def debug(self, msg):
        if self.debug:
            cf = currentframe()
            print(f"[#{cf.f_back.f_lineno}] {msg}")

class DateTime:
    def __init__(self, timezone=''):
        if timezone != '':
            os.environ['TZ'] = timezone
    def datetime_from_str(self, s):
        date_pattern = r"[1-3][0-9][\/\-\ ][0-1][0-9][\/\-\ ][1-2][0-1][0-9][0-9]|"
        us_time_pattern = r"((1[0-2]|0?[1-9])[:\.]([0-5][0-9]) ?([AaPp][Mm]))"
        return parser.parse(s)
    def get_unix(self, s):
        return self.datetime_from_str(s).timestamp()
