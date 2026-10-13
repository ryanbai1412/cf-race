"""Source-backed Grammar Lessons recipe; not a qualification or audit."""
import itertools
import random
import re


IDS = ('113A',)
SEMANTICS = {
    '113A': 'One nonempty line of lowercase Latin words with exactly one space '
    'between words, no other spaces, at most 100000 characters excluding the '
    'line terminator (public English HTML attests 10^5; upstream flattened 105). '
    'Only final suffixes lios/liala, etr/etra, initis/inites determine '
    'adjective/noun/verb and masculine/feminine gender. A single valid word '
    'is a sentence; otherwise require one gender and adjective* noun verb*. '
    'Unique YES/NO; linear suffix/phase oracle checked against independent '
    'whole-sentence regular grammars over exhaustive small sequences.'
}

_ENDINGS = (
    ('lios', 0, 0), ('liala', 1, 0),
    ('etr', 0, 1), ('etra', 1, 1),
    ('initis', 0, 2), ('inites', 1, 2),
)
_INPUT = re.compile(r'[a-z]+(?: [a-z]+)*')
_BRUTE_GRAMMARS = tuple(map(re.compile, (
    r'[a-z]*(?:lios|liala|etr|etra|initis|inites)',
    r'(?:[a-z]*lios )*[a-z]*etr(?: [a-z]*initis)*',
    r'(?:[a-z]*liala )*[a-z]*etra(?: [a-z]*inites)*',
)))


def _require_id(pid):
    if pid != '113A':
        raise ValueError('unsupported problem ID')


def parse(pid, text):
    _require_id(pid)
    if not isinstance(text, str):
        raise ValueError('input must be text')
    line = text
    if line.endswith('\n'):
        line = line[:-1]
        if line.endswith('\r'):
            line = line[:-1]
    if not 1 <= len(line) <= 100000:
        raise ValueError('line character count must be 1..100000')
    if _INPUT.fullmatch(line) is None:
        raise ValueError('expected one lowercase-word line with single spaces')
    return tuple(line.split(' '))


def _classify(word):
    for ending, gender, part in _ENDINGS:
        if word.endswith(ending):
            return gender, part
    return None


def answer(pid, data):
    _require_id(pid)
    gender = None
    phase = 0
    nouns = 0
    for word in data:
        kind = _classify(word)
        if kind is None:
            return 'NO'
        current_gender, part = kind
        if gender is not None and current_gender != gender:
            return 'NO'
        gender = current_gender
        if part < phase:
            return 'NO'
        phase = part
        nouns += part == 1
        if nouns > 1:
            return 'NO'
    return 'YES' if data and (len(data) == 1 or nouns == 1) else 'NO'


def _brute_answer(words):
    text = ' '.join(words)
    return 'YES' if any(pattern.fullmatch(text) for pattern in _BRUTE_GRAMMARS) else 'NO'


def extras(pid):
    _require_id(pid)
    cases = []
    seen = set()

    def add(words, reason, category='adversarial'):
        text = ' '.join(words) + '\n'
        if text in seen:
            return
        data = parse(pid, text)
        seen.add(text)
        cases.append({'input': text, 'output': answer(pid, data) + '\n',
                      'reason': reason, 'category': category})

    symbols = ('lios', 'liala', 'etr', 'etra', 'initis', 'inites', 'a')
    for word in symbols:
        add([word], 'Single ending is a word, including adjective/verb; a is the minimum invalid word.', 'boundary')
    for words in itertools.product(symbols, repeat=2):
        add(words, 'Every two-word type/gender/invalid combination: noun required and order matters.', 'boundary')

    witnesses = (
        (('etr', 'etr', 'initis'), 'Exactly one noun, not merely nondecreasing part order.'),
        (('lios', 'etr', 'initis', 'lios'), 'A valid prefix followed by a late adjective: reject prefix-only regex matching.'),
        (('liala', 'etra', 'inites', 'etra'), 'Second feminine noun after a valid sentence.'),
        (('etr', 'initis', 'etr'), 'Second masculine noun after a verb.'),
        (('lios', 'lios', 'lios'), 'Several adjectives are not the single-word exception.'),
        (('liala', 'liala', 'liala'), 'Feminine adjectives alone still need a noun.'),
        (('initis', 'initis', 'initis'), 'Several verbs are not a sentence.'),
        (('inites', 'inites', 'inites'), 'Feminine verbs alone are not a sentence.'),
        (('a', 'lios', 'etr', 'initis'), 'An invalid early word cannot be overwritten by valid later words.'),
        (('lios', 'etr', 'a', 'initis'), 'An invalid middle word cannot be ignored.'),
        (('lios', 'etr', 'initis', 'a'), 'Invalid final word after a valid sentence.'),
        (('lios', 'etra', 'initis'), 'A single opposite-gender noun breaks agreement.'),
        (('liala', 'etra', 'initis'), 'A single opposite-gender verb breaks agreement.'),
        (('liala', 'etr', 'initis'), 'A single opposite-gender adjective breaks agreement.'),
        (('initis', 'lios', 'etr'), 'Verb before adjective and noun.'),
        (('etr', 'lios', 'initis'), 'Adjective after noun.'),
        (('liala', 'inites', 'etra'), 'Verb before noun.'),
        (('lioslialapetrpetrainitisiniteslios', 'petrainitisetr', 'lialainitis'), 'Only final suffix matters, not an earlier embedded ending.'),
        (('etr', 'xxinitisetr'), 'A verb-looking prefix does not turn a second noun into a verb.'),
        (('etrx',), 'Recognized ending inside a word is not a final suffix.'),
        (('lioss',), 'One extra letter destroys an otherwise valid ending.'),
        (('ini',), 'Short proper prefix of an ending is not a word.'),
    )
    for words, reason in witnesses:
        add(words, reason)
    for gender in range(2):
        adjective, noun, verb = (('lios', 'etr', 'initis'), ('liala', 'etra', 'inites'))[gender]
        for adjectives in range(4):
            for verbs in range(4):
                words = ['q' + adjective] * adjectives + ['qq' + noun] + ['qqq' + verb] * verbs
                add(words, 'Both genders; zero through three adjectives/verbs around the sole noun.', 'boundary')
    for ending, _, _ in _ENDINGS:
        add([ending[:-1]], 'Truncating an ending creates an invalid language word.')
        add([ending + 'x'], 'An ending followed by x is not recognized.')
        add(['lioslialaetretrainitisinites' + ending], 'Gender/part are determined by the final ending alone.')

    for ending, _, _ in _ENDINGS:
        add(['x' * (100000 - len(ending)) + ending], 'Exactly 100000 characters: one valid word, arbitrary long prefix.', 'maxSize')
    add(['a' * 100000], 'Exactly 100000 characters: one invalid word.', 'maxSize')
    add(['a'] * 49999 + ['aa'], 'Exactly 100000 characters and the maximum 50000 nonempty words.', 'maxSize')
    add(['zzlios'] + ['lios'] * 19998 + ['etr'], 'Exactly 100000 characters: 19999 adjectives then one noun.', 'maxSize')
    add(['zlios'] + ['lios'] * 19999, 'Exactly 100000 characters: 20000 adjectives, missing noun.', 'maxSize')
    add(['zzetr'] + ['initis'] * 14285, 'Exactly 100000 characters: one noun then 14285 verbs.', 'maxSize')
    add(['zzetr'] + ['initis'] * 14284 + ['initix'], 'Exactly 100000 characters: invalid word only at the final position.', 'maxSize')

    rng = random.Random(1600113)
    while len(cases) < 160:
        if len(cases) % 2 == 0:
            adjective, noun, verb = rng.choice((('lios', 'etr', 'initis'), ('liala', 'etra', 'inites')))
            endings = [adjective] * rng.randrange(6) + [noun] + [verb] * rng.randrange(6)
        else:
            endings = [rng.choice(symbols) for _ in range(rng.randint(1, 10))]
        words = [''.join(rng.choice('aeilnorst') for _ in range(rng.randrange(9))) + ending for ending in endings]
        add(words, 'Fixed-seed small random prefixes and grammatical/type/gender sequences.')
    return cases


def review(pid, tests, samples):
    _require_id(pid)
    failures = []
    for name, pair in itertools.chain(tests, samples):
        try:
            expected = answer(pid, parse(pid, pair['input']))
            if pair['output'].split() != [expected]:
                failures.append({'test': name, 'reason': 'oracle output differs from supplied bytes',
                                 'expected': expected, 'actual': pair['output'].split()})
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures


def brute_checks():
    count = 0

    def check(words):
        nonlocal count
        expected = _brute_answer(words)
        actual = answer('113A', words)
        if actual != expected:
            raise AssertionError((words, expected, actual))
        count += 1

    symbols = ('lios', 'liala', 'etr', 'etra', 'initis', 'inites', 'a')
    for length in range(1, 6):
        for words in itertools.product(symbols, repeat=length):
            check(words)
    for length in range(1, 5):
        for letters in itertools.product('aeilnorst', repeat=length):
            check((''.join(letters),))
    rng = random.Random(1131600)
    for _ in range(500):
        words = []
        for _ in range(rng.randint(1, 12)):
            prefix = ''.join(rng.choice('aeilnorst') for _ in range(rng.randrange(12)))
            ending = rng.choice(symbols + ('liosx', 'et', 'ini', 'initex'))
            words.append(prefix + ending)
        check(words)
    for case in extras('113A'):
        check(parse('113A', case['input']))
    return {'113A': count}
