"""
# Advent day 01

The newly-improved calibration document consists of lines of text;
each line originally contained a specific calibration value that the Elves now need to recover.
On each line, the calibration value can be found by combining the first digit and the last digit
(in that order) to form a single two-digit number.

For example:

    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77.
Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

# My thoughts

Seems pretty simple, so I want to do this the most generic way possible without
using modules. It's the kind of thing I'd love to do in C if I actually remembered
the language. Walking across each string, getting each character, saving the first
and last and totalling them up at the end. Save memory by tallying them up as we
go, and heck, only three reusable variables are needed, well.. and the flag to
test when the first was found.

"""

# -------------------------------------------------
# Solution
# -------------------------------------------------

from .utils import Utils              # I won't explain this in subsequent problems, in hopes it'll remain consistent, but..
u = Utils(__file__)                   # ..these utilities assign file names, etc., based on this Day's number, captured from this file name...

total = 0
with open(f'{u.inbase}.txt') as f:    # ..in case we might use CSVs or other input, I left off the extension from the utility's input file name.
  for line in f.readlines():
    first = last = 0                  # I wanna save the integers rather than the chars from the get-go
    gotfirst = False                  # hmm, could I do this without the flag test?
    for c in line:                    # walk each character L -> R in the string ( C getchar() )
      if c >= '0' and c <= '9':       # I'm guessing that ASCII char comparisons might be the cheapest test?
        if gotfirst:
          last = int(c)               # first never changes, of course
        else:
          first = last = int(c)       # capture first AND, according to the problem spec, the first digit is the first-possible last digit
          gotfirst = True             # <-- forgot to flip this switch the first time (Doh!)
    total += (first*10) + last        # first number is always in the 10s position, even if 0

u.output(f'Calibration value sum: {total}')   # This captures the solution in a `{DD}-results.txt` file.
