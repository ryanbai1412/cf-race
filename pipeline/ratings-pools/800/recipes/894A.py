from rlib import *

CONSTRAINTS = "one string of 1..100 uppercase letters."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: number of QAQ subsequences."


def validate(inp):
    word(exact_tokens(inp, 1)[0], UPPER, 1, 100)


def solve(inp):
    s = inp.split()[0]
    q = qa = qaq = 0
    for c in s:
        if c == "Q":
            qaq += qa; q += 1
        elif c == "A":
            qa += q
    return str(qaq)


def extra():
    return [("boundary", "single Q", "Q\n"), ("boundary", "exact QAQ", "QAQ\n"), ("adversarial", "AQQA no match", "AQQA\n"),
            ("maxSize", "33 Q, 34 A, 33 Q (max count)", "Q" * 33 + "A" * 34 + "Q" * 33 + "\n"), ("maxSize", "QA repeated", "QA" * 50 + "\n")]
