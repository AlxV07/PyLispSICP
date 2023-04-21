"""
Fill in the missing expressions to complete the following definitions of some basic list-manipulation operations
as accumulations:

1.
def map(p, sequence):
    return accumulate(lambda x, y: (???), None, sequence)

2.
def append(seq1, seq2):
    return accumulate(cons, (???), (???))

3.
def length(seq):
    return accumulate((???), 0, seq)
"""
from chapter_two.one_one.mock_scheme_lisp_pair import cons
from chapter_two.two_two.accumulate_process import accumulate


# 1.
def map_accumulate_version(p, sequence):
    return accumulate(lambda x, y: cons(p(x), y), None, sequence)


# 2.
def append_accumulate_version(seq1, seq2):
    return accumulate(cons, seq2, seq1)  # WIP


# 3.
def length_accumulate_version(seq):
    return accumulate(lambda x, y: 1 + y, 0, seq)
