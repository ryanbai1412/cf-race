"""CF-style token checker (mirrors the judge contract in docs/JUDGE_API.md)."""


def tokens(text: str):
    return text.split()


def check(expected: str, actual: str, float_eps=None) -> bool:
    et, at = tokens(expected), tokens(actual)
    if len(et) != len(at):
        return False
    for e, a in zip(et, at):
        if e == a:
            continue
        if e.lower() in ("yes", "no") and e.lower() == a.lower():
            continue
        if float_eps is not None:
            try:
                fe, fa = float(e), float(a)
                if abs(fe - fa) <= float_eps or (
                    fe != 0 and abs(fe - fa) / abs(fe) <= float_eps
                ):
                    continue
            except ValueError:
                pass
        return False
    return True
