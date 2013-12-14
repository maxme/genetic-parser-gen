from difflib import SequenceMatcher

def compare_criterias(i1, c2):
    s = SequenceMatcher(None, i1.crits["rowdata"], c2["rowdata"])
    return s.ratio()
