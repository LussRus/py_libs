'''
    Created 22.07.2022 by DenisSh
'''
import re


class convert_number:
    def __init__(self):
        self.s = ['%', 'K', 'M', 'B']

    def get(self, s):
        s = re.sub(r'[, ]', '', s)
        symbs = re.findall('%', s)
        if len(symbs) == 0:
            symbs = re.findall(r'[BMK]', s)
            if len(symbs) == 0:
                return float(s)
        symb = symbs[0]
        val = float(s.replace(symb, ''))
        return val * (1000 ** self.s.index(symb))

    def money(self, v):
        znak = ''
        if v < 0:
            v = v * -1
            znak = '-'
        if v < 1:
            return str(v)
        for i in reversed(range(4)):
            s = ''
            r = v / 1000 ** i
            if int(r) > 1:
                s = str(round(r, 2)) + self.s[i]
                break
        return znak + s

    def diff(self, s1, s2):
        v1 = self.get(s1)
        v2 = self.get(s2)
        diff = v2 - v1
        if '%' in s1:
            return str(round(diff, 2)) + '%'
        return self.money(diff)

    def diff_perc(self, s1, s2):
        v1 = self.get(s1)
        v2 = self.get(s2)
        diff = v2 - v1
        res = str(round(diff / v1 * 100, 2)) + '%'
        if '%' in s1:
            return res + '%'
        return res

    def split(self, v):
        print(isinstance(v, str))
        if isinstance(v, str):
            v = self.get(v)
        res = re.sub("(\d)(?=(\d{3})+(?!\d))", r'\1 ', "%.17g" % v)
        return res
