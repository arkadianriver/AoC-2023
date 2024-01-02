"""
# Day 01

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

## My thoughts

Seems pretty simple, so I want to do this the most generic way possible without
using modules. It's the kind of thing I'd love to do in C if I actually remembered
the language. Walking across each string, getting each character, saving the first
and last and totalling them up at the end. Save memory by tallying them up as we
go, and heck, only three reusable variables are needed, well.. and the flag to
test when the first was found.

## `--- Part Two ---`

Your calculation isn't quite right. It looks like some of the digits are actually spelled out
with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line.
For example:

	two1nine
	eightwothree
	abcone2threexyz
	xtwone3four
	4nineeightseven2
	zoneight234
	7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76.
Adding these together produces 281.

What is the sum of all of the calibration values?

## My thoughts on Part Two

Okay, I didn't know there was a part two until solving part one.

For part two, I could use `"".replace()` to substitute digits first and
subsequently leave the rest of the logic the same.

But, I think I'll try to do it in one pass first, changing the for loop
to a while string-is-not-empty and a getchar function to inch forward
char-by-char to see if it matches a digit, keeping the rest of the logic
the same. Note that Python doesn't mutate strings, so I'll use the
convention of a cursor, called 'pos' (to note the position in the string).

I'll also break it up into functions so that we can:

- run either part 1 or part two
- preserve the first, last, total logic for either

Okay, let's tweak that a bit because I read in a comment that `sevenine` would
be considered 79 rather than 77. So, I'll do this differently. Instead of
going from left to right all the way through, since we need only the first
and last, I'll go from the left to get the first, then stop and go in from the right
to get the last. That should do the trick. When coming in from the right, I'll spell
the numbers in reverse.

"""

# -------------------------------------------------
# Solution
# -------------------------------------------------

from .utils import Utils              # I won't explain this in subsequent problems, in hopes it'll remain consistent, but..
u = Utils(__file__)                   # ..these utilities assign file names, etc., based on this Day's number, captured from this file name...

# Part 1.

def part_1():
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

	u.store_content(f'# part 1:\n  Calibration value sum: {total}\n')   # captures the result for later reporting.


# Part Two.

## helpers

def _getchar(line, pos, reverse=False):
	'''gets the next (or previous) char and increments the position by one.
	   returns _current_ character but next (or previous) position.'''
	try:
		c = line[pos]
		p = pos-1 if reverse else pos+1
	except IndexError:
		c = ''
		p = -1
	return (c, p)

def _is_digit(line, c, pos, spelled_digit, reverse=False):
	'''loops through the spelled digit to see if the next chars in line are a match.
	   the character and position are returned later in the calling _build_digit function.'''
	for i in spelled_digit:
		(c, pos) = _getchar(line, pos, reverse=reverse)
		if c != i:
			return False
	return True

def _build_digit(line, c, pos, reverse=False):
	'''returns digit for spelled digit if matched (and new position);
	    otherwise, just returns the same character and position.
			Using a data structure for the values so that I don't have to keep
			retyping the condition, _is_digit, and return over and over'''
	map = {
			'e': [('no', '1', 2), ('erht', '3', 4), ('vif', '5', 3), ('nin', '9', 3)],
			'o': [('wt', '2', 2)], 'r': [('uof', '4', 3)], 'x': [('is', '6', 2)],
			'n': [('eves', '7', 4)], 't': [('hgie', '8', 4)]
		} if reverse else {
			'o': [('ne', '1', 2)], 't': [('wo', '2', 2), ('hree', '3', 4)],
			'f': [('our', '4', 3), ('ive', '5', 3)], 's': [('ix', '6', 2), ('even', '7', 4)],
			'e': [('ight', '8', 4)], 'n': [('ine', '9', 3)]
		}
	for k, v in map.items():
		if c == k:
			for (spelled, digit, delta) in v:
				if _is_digit(line, c, pos, spelled, reverse=reverse):
					new_pos = pos - delta if reverse else pos + delta
					return (digit, new_pos)
	return (c, pos)

## driver

def part_two():
	'''This time, going in from left for first and from right for last'''
	total = 0
	with open(f'{u.inbase}.txt') as f:
		for line in f.readlines():
			line = line.strip()
			first = last = 0

			# get first (from left)
			pos = 0
			while pos >= 0:                             # keep looping if the string isn't empty (pos not -1)
				(c, pos) = _getchar(line, pos)            # can't pass by reference (pointers) in Python, so re-assigning pos instead
				if c in 'otfsen':                         # first letters of spelled digits
					(c, pos) = _build_digit(line, c, pos)   # if it spells a digit, return it and the updated position
				if c >= '0' and c <= '9':                 # now cleaned of any spelled digits, we can test if c has what we want
					first = int(c)
					break

			# get last (from right)                         # same but backwards (using reverse flag in functions as appropriate)
			pos = len(line) - 1                             # starting from last index
			while pos >= 0:                                 # getchar still conveniently uses -1 as end of string in reverse as well
				(c, pos) = _getchar(line, pos, reverse=True)
				if c in 'eorxnt':                             # _last_ letters of spelled digits
					(c, pos) = _build_digit(line, c, pos, reverse=True)
				if c >= '0' and c <= '9':
					last = int(c)
					break
			total += (first*10) + last

	u.store_content(f'# part two:\n  Calibration value sum: {total}\n')


def main():
	part_1()
	part_two()
	u.report()  # Reports the collected output to a `day_{DD}-results.txt` file.

if __name__=="__main__":
	main()
