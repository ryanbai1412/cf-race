"""Materialize source-bound, not-yet-audited mathematical-WA candidates."""
import argparse
import hashlib
import json

from correction_triage import indexed_sources


PROPOSALS = {
    "118A": ("221238567", "0090", "Omits Y/y from the vowel set; retains a y that must be removed from the dotted output."),
    "13A": ("24147486", "0003", "At an integer power, ceil(log(n,base)) can give the wrong digit count: 1000 in base 10 is treated as a leading digit 10, corrupting the digit sum."),
    "259A": ("34953556", "0009", "Checks only the total number of white cells, not whether each row alternates colors; 32 white squares are not sufficient."),
    "265B": ("86313287", "0004", "Initializes the path computation using the last height at i=0 and ignores the initial ascent; a single height of 10000 requires 10001 moves, not two."),
    "29A": ("59110844", "0005", "Tests absolute distance against signed spit displacement; misses mutually spitting statues with negative first displacement."),
    "389A": ("10261655", "0005", "Uses the minimum adjacent value difference times n, which is zero for equal adjacent values but the required result for [1,1] is two."),
    "535A": ("13720030", "0059", "Uses the tens digit instead of the units digit to select the second word; 41 is incorrectly rendered as forty-four."),
    "583A": ("13507609", "0003", "Prints a hardcoded n+1 stride schedule regardless of visited intersections; (1,1),(2,2) has days 1 and 2, not 1 and 4."),
    "628A": ("16731139", "0001", "Uses a power of two strictly above the remaining players for matches, overcounting bottles for five players."),
    "641A": ("27865969", "0013", "Sums jump displacements once instead of detecting revisited in-strip positions; a cycle is incorrectly classified FINITE."),
    "660B": ("63712502", "0006", "Interleaves seat indices using the bus capacity rather than the first m occupied seats; returns 6,1,7,2... instead of 1..10."),
    "766B": ("131298859", "0002", "The first triangle check wraps to a[-1] via i-1, so lengths 1,2,4 are incorrectly accepted."),
    "74A": ("105601402", "0006", "Awards 50 rather than 100 points per successful hack; 5 successes plus 199 problem points then incorrectly beats 7 successes."),
    "465B": ("53192298", "0004", "Assumes one extra operation beyond the number of unread letters; alternating unread/read letters require nine operations, not six."),
}

EXCLUSIONS = {
    "13A": ["9095133", "14495296", "15070377", "20894819"],
    "535A": ["10761957", "10819786"],
    "660B": ["17689898"],
    "74A": ["4699469", "6570394"],
}

EXCLUSION_REASONS = {
    "9095133": "Unreduced but mathematically equal fraction; not an algorithmic value witness.",
    "14495296": "Spaces around slash; numeric rational value is correct.",
    "15070377": "Unreduced but mathematically equal fraction; not an algorithmic value witness.",
    "20894819": "Debug dictionary before the computed fraction.",
    "10761957": "Spells eighty as eigthy; presentation-only difference.",
    "10819786": "Input prompt and forty misspelling; not a mathematical value witness.",
    "17689898": "Prints debug n,m before the passenger order.",
    "4699469": "Initial maximum -1 suppresses the winner on all-negative scores. Conservatively replaced by a valid-name mathematical witness.",
    "6570394": "Initial maximum zero suppresses the winner on nonpositive scores. Conservatively replaced by a valid-name mathematical witness.",
}

EXTRA = {
    "13A": [
        ("49561748", "0003", "Missing parentheses in n-2//gcd gives the wrong denominator, 999 instead of 499."),
        ("56854758", "0003", "Counts the length of a decimal concatenation of base digits rather than summing the base digit values."),
        ("83370980", "0003", "Unconditionally adds one when repeated division terminates at zero, overcounting sums for bases with zero final quotient."),
        ("26645184", "0003", "Concatenates base digit values then sums their decimal characters, corrupting digit values greater than nine."),
    ],
    "535A": [
        ("10820192", "0009", "Omits zero and uses a negative lookup index, mapping zero to forty."),
        ("25421115", "0009", "Omits the zero entry from the one-digit lookup table, mapping zero to nine."),
    ],
    "660B": [("89308978", "0006", "Uses m/2 to partition passengers without considering bus rows; ten window passengers incorrectly interleave two halves.")],
    "74A": [
        ("121414873", "0006", "Adds successes per nonzero problem rather than 100 per successful hack; 5 successes plus 199 points incorrectly beats 7 successes."),
        ("12583673", "0004", "Sorts the dictionary keys rather than the computed scores, selecting the lexicographically greatest name."),
    ],
}

WITNESS_OVERRIDES = {
    "118A": {sid: "0090" for sid in ["220822513", "220905950", "220933558", "221011266"]},
    "660B": {"17399963": "0006"},
}


def source_record(pid, sid, witness, defect):
    matches = [r for r in indexed_sources(pid) if str(r["submission_id"]) == sid]
    if len(matches) != 1 or matches[0]["verdict"] != "WRONG_ANSWER" or matches[0]["testset"] != "TESTS":
        raise ValueError(f"unpinned or ambiguous public wrong reference: {pid}/{sid}")
    row = matches[0]
    return {"submissionId": sid, "sourceHash": hashlib.sha256(row["source"].encode()).hexdigest(),
            "test": witness, "defect": defect}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    records = {}
    for pid, (sid, witness, defect) in PROPOSALS.items():
        records[pid] = source_record(pid, sid, witness, defect)
        if pid in EXCLUSIONS:
            records[pid]["excludePreviouslyClaimed"] = EXCLUSIONS[pid]
            records[pid]["excludedPriorReferenceReasons"] = {
                sid: {"sourceHash": source_record(pid, sid, "", "")["sourceHash"],
                      "reason": EXCLUSION_REASONS[sid]}
                for sid in EXCLUSIONS[pid]
            }
        if pid in EXTRA:
            records[pid]["additionalReplacements"] = [source_record(pid, *r) for r in EXTRA[pid]]
        if pid in WITNESS_OVERRIDES:
            records[pid]["retainedWitnessOverrides"] = WITNESS_OVERRIDES[pid]
    with open(args.output, "w") as output:
        json.dump(records, output, indent=2, sort_keys=True)
        output.write("\n")


if __name__ == "__main__":
    main()
