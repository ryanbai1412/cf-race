"""Pin candidate source defects for fresh external review, not validation."""
import argparse
import json

from correction_selection_batch02 import source_record


PROPOSALS = {
    "102B": [
        ("90308825", "0005", "Prints digit count rather than iterations of digit sum; 100 needs one iteration, not three."),
        ("90486603", "0003", "Returns final digital root instead of the number of digit-sum operations; 991 needs three."),
        ("211288152", "0001", "Computes final digital root but returns its digit length rather than counting operations; zero needs none."),
    ],
    "118B": [
        ("231247155", "0001", "Emits only ascending rows without mirrored right-half digits; at n=2 the center must be 0 1 2 1 0."),
    ],
    "182B": [
        ("53369961", "0001", "Excludes every station sharing the final station's rest time, instead of only the final stop."),
        ("62783412", "0001", "Includes the final stop's time among the waited minutes; there is no wait after arrival."),
    ],
    "284B": [
        ("14297326", "0004", "Scans one-character-short prefixes and skips the wrong position; misses surviving A supporters."),
        ("25759596", "0004", "Treats one I supporter as none and counts A rather than applying the I-dominates rule."),
    ],
    "336A": [
        ("4596787", "0003", "Wrong intercept signs for positive x, negative y; the candidate segment does not pass through the point."),
        ("4596856", "0002", "Wrong intercept signs for negative x, positive y; the candidate segment does not pass through the point."),
    ],
    "400A": [
        ("53117043", "0001", "Counts rows of X's rather than a completely filled column, yielding legal but infeasible layouts."),
    ],
    "404A": [
        ("80000612", "0004", "Checks rows without enforcing the diagonal/background constraints throughout the grid."),
        ("80392064", "0007", "Accepts any palindrome grid without requiring two distinct uniform X letters."),
        ("80544707", "0007", "Accepts a symmetric grid without checking all off-diagonal cells and distinct letters."),
    ],
    "447B": [
        ("7092647", "0002", "Appends character positions using k+1..2k, not len(s)+1..len(s)+k."),
        ("7123806", "0001", "Sums letter weights without multiplying each by its one-based position."),
        ("7151369", "0002", "Omits w from the alphabet-weight mapping, shifting the x/y/z weights."),
    ],
    "620B": [
        ("15477405", "0003", "Incorrectly aggregates hundreds blocks' zero displays when counting seven-segment lights."),
        ("15479855", "0003", "Compares a string digit to integer zero, never updating carry changes in display counts."),
    ],
    "622A": [
        ("16073456", "0001", "Reverses the loop condition and returns n without consuming triangular groups."),
        ("16400452", "0001", "Subtracts the previous triangular total rather than selecting the number at position n."),
        ("25576856", "0005", "Uses n-i rather than the position inside the current triangular group."),
        ("28468063", "0002", "Increments the block size by two instead of one."),
        ("29043587", "0001", "Off-by-one in the derived group formula selects the wrong array value."),
    ],
    "725A": [
        ("21760805", "0004", "Uses an incorrect reverse-index formula for trailing > direction count."),
        ("21813767", "0001", "Adds the non-escaping middle to the escaping edge counts."),
        ("22053680", "0004", "Counts global arrow imbalance instead of outward-facing edge arrows."),
        ("22053848", "0004", "Counts global arrow imbalance instead of outward-facing edge arrows."),
    ],
    "742A": [
        ("145924089", "0002", "Uses the tens digit of n rather than n mod 4 for the final power of eight."),
        ("145924448", "0021", "Maps the exponent remainder to the wrong last digit."),
    ],
    "777A": [
        ("24986339", "0005", "Treats rotating shell positions as an additive three-cycle instead of alternating swaps."),
        ("24996752", "0007", "Uses a length-seven permutation cycle instead of the actual six-operation cycle."),
        ("24999378", "0005", "Selects an incorrect six-operation permutation for the starting shell."),
    ],
    "804A": [
        ("27146063", "0004", "Subtracts one from floor(n/2), an off-by-one for odd n."),
        ("27699229", "0004", "Combines the odd-n branch with an extra n/2 term rather than floor(n/2)."),
    ],
    "886B": [
        ("32317833", "0004", "Outputs the reverse-list index instead of the chosen canteen value."),
        ("32341376", "0004", "Tracks a repeated value's offset instead of the canteen requested latest."),
        ("32350638", "0001", "Initializes the minimum at minus one; no nonnegative last-seen index can replace it."),
        ("32979247", "0003", "Reverses the text of each number rather than visit order, and defaults to one when none is found."),
    ],
    "990A": [
        ("39115520", "0006", "Compares arbitrary n to 2m rather than the nearest multiple of m."),
        ("39124800", "0011", "Multiplies m by increasing factors rather than finding the nearest multiple of m."),
    ],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    records = {}
    for pid, entries in sorted(PROPOSALS.items()):
        refs = [source_record(pid, sid, witness, defect) for sid, witness, defect in entries]
        records[pid] = {**refs[0], "additionalReplacements": refs[1:]}
    with open(args.output, "w") as output:
        json.dump(records, output, indent=2, sort_keys=True)
        output.write("\n")


if __name__ == "__main__":
    main()
