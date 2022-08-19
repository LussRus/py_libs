from inspect import currentframe
from datetime import datetime
import re
import time

DEBUG = True

class roll:
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

def debug(msg):
    if DEBUG:
        cf = currentframe()
        print(f"[#{cf.f_back.f_lineno}] {msg}")

def get_linenumber():
    cf = currentframe()
    return f"[#{cf.f_back.f_lineno}]"

def mark_fat(str):
    res = str
    els = re.findall(r"\d.*?%|\$.*?\s", str)
    for el in els:
        res = res.replace(el, "<strong>"+el+"</strong>")
    return res

def format_message_from_el(msg, sect):
    res = ""
    res += f"\n<a href=\"{msg['link']}\"><b>{msg['title']}</b></a>"
    res += '\n'
    res += mark_fat( msg['text'] )
    res += '\n'
    res += f"{msg['datetime_str']}   <i>{msg['author']}</i>  <b><i>({sect[:1]})</i></b>"
    return res

rus_text_replacement = {"АНАЛИЗ — ": "", "Конференц-звонок ": "Созвон будет: ", "Конференц-связь ": "Общее обсуждение: "}
def replace_some_words_in_rus_text(txt):
    for k in rus_text_replacement.keys():
        answ_text = txt.replace(k, rus_text_replacement[k])
    return answ_text

def format_rus_mess(msg, sect):
    res = ""
    res += f"\n<a href=\"{msg['link']}\"><b>{ replace_some_words_in_rus_text(msg['rus_title']) }\n({msg['title']})</b></a>"
    res += '\n'
    res += mark_fat( msg['rus_text'] )
    res += '\n'
    res += f"{msg['datetime_str']}   <i>{msg['author']}</i>  <b><i>({sect[:1]})</i></b>"
    return res

def parse_pubdate(str):
    dt = datetime.strptime(str[5:-6], '%d %b %Y %H:%M:%S')
    return dt# 'Tue, 05 Jul 2022 14:00:14 +0000'

def unix_time(s):
    return int(time.mktime(datetime.strptime(s, "%H:%M %d-%m-%Y").timetuple()))
