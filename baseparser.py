from primitives import *
from io import StringIO
import pickle
import csv
import re


class BaseParser:
    data = ""

    def __init__(self):
        self._str_ops = []
        self._s2l_ops = []
        self._clean_ops = []

    def load_data(self, filename):
        stream = open(filename)
        self.data = stream.read()

    def run_clean_ops(self, l):
        for op in self._clean_ops:
            for n, line in enumerate(l):
                l[n] = op(line)
        return l

    def run_str_ops(self, s):
        for op in self._str_ops:
            s = op(s)
        return s

    def run_s2l_ops(self, s):
        l = []
        curre = re.compile("".join([i[0] for i in self._s2l_ops]).strip())
        try:
            for match in curre.findall(s):
                l.append(list(match))
        except KeyboardInterrupt as e:
            print(("".join([i[0] for i in self._s2l_ops])))
            raise e
        return l

    def run_all(self):
        s = self.run_str_ops(self.data)
        self.parsed = self.run_s2l_ops(s)
        self.parsed = self.run_clean_ops(self.parsed)
        return self.parsed

    def csv_dump(self):
        tmp = StringIO()
        csvwriter = csv.writer(tmp, quoting=csv.QUOTE_ALL, lineterminator="\n")
        for i in self.parsed:
            csvwriter.writerow(i)
        return tmp.getvalue()  # .replace('","', '"###,###"')

    def criterias(self):
        self.crits = {"len": len(self.parsed), "rowdata": self.csv_dump()}
        return self.crits

    def st(self):
        return "filters: %s\nregex: %s\ncleaners: %s\n" % (
            ", ".join([i.__name__ for i in self._str_ops]),
            "".join([i[0] for i in self._s2l_ops]),
            ", ".join([i.__name__ for i in self._clean_ops]),
        )

    def dump(self, filename):
        stream = open(filename, "wb")
        pickle.dump((self._str_ops, self._s2l_ops, self._clean_ops), stream)
        stream.close()

    def load(self, filename):
        stream = open(filename, "rb")
        self._str_ops, self._s2l_ops, self._clean_ops = pickle.load(stream)
        stream.close()


if __name__ == "__main__":
    import sys

    bp = BaseParser()
    bp.load(sys.argv[1])
    bp.load_data(sys.argv[2])
    print((bp.run_all()))
