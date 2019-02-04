import re

# string primitives
def str_remove_tabs(s):
    return s.replace("\t", " ")


def str_remove_endline(s):
    return s.replace("\n", " ")


def str_remove_consecutive_spaces(s):
    return re.sub(r"\ +", " ", s)


def str_strip(s):
    return s.strip()


def str_replace_comma(s):
    return s.replace(",", " ")


def str_replace_whitespace(s):
    return s.replace(" ", ",")


# regexp primitives
s2l_date1 = ("([0-9]{2}/[0-9]{2})", 1)
s2l_date2 = ("([0-9]{2}/[0-9]{2}/[0-9]{2})", 1)
s2l_date2 = ("([0-9]{2}/[0-9]{2}/[0-9]{4})", 1)
s2l_float = ("(-?[0-9]{1,20}[.,]+[0-9]{1,20})", 1)
s2l_int = ("(-?[0-9]{1,20})", 1)

s2l_everything_nongreedy = ("(.{1,100}?)", 0)
s2l_everything_nongreedy_remove = (
    ".{1,100}?",
    0,
)  # arbitrary chosen 100 limit because of : http://www.regular-expressions.info/catastrophic.html

s2l_endline = ("(\n)", 1)
s2l_endline_remove = ("\n", 1)

s2l_whitespace = ("(\s)", 1)
s2l_whitespace_remove = ("\s", 1)

s2l_seps = ("(['\"\-+,;:\. ])", 1)
s2l_seps_remove = ("['\"\-+,;:\. ]", 1)

# clean primitives
def clean_strip(l):
    """
    >>> clean_strip(["a ", "", "  c   "])
    ['a', '', 'c']
    """
    for n, elt in enumerate(l):
        l[n] = elt.strip()
    return l


def clean_empty(l):
    """
    >>> clean_empty(["a", "", "c"])
    ['a', 'c']
    """
    return list(filter(lambda x: x != "", l))


def merge(n=1):
    """
    >>> merge(1)(["a", "b", "c"])
    ['ab', 'c']
    >>> merge(2)(["a", "b", "c"])
    ['a', 'bc']
    >>> merge(3)(["a", "b", "c"])
    ['a', 'b', 'c']
    """

    def _in(l):
        if len(l) < n + 1:
            return l
        l[n - 1] += l.pop(n)
        return l

    return _in


for i in range(1, 10):
    locals()["clean_merge%d" % i] = merge(i)

str_primitives = [eval(i) for i in filter(lambda x: x.startswith("str"), dir())]
clean_primitives = [eval(i) for i in filter(lambda x: x.startswith("clean"), dir())]
re_primitives = [eval(i) for i in filter(lambda x: x.startswith("s2l"), dir())]

if __name__ == "__main__":
    # python3 primitives.py -v
    import doctest

    doctest.testmod()
