import os, re
import subprocess

class Utils():

	def __init__(self, filename):
		self.filename = filename
		self.dp0 = os.path.dirname(os.path.realpath(filename))
		self.a_day = os.path.splitext(os.path.basename(filename))[0][4:6]
		self.inbase = f'{self.dp0}/day_{self.a_day}-input'
		self.output = ''

	def store_content(self, content):
		self.output += content

	def report(self, debug=False):
		if debug:
			print(self.output)
		else:
			with open(f'{self.dp0}/day_{self.a_day}-results.txt', 'w', encoding='utf-8') as of:
				of.write(self.output)

def list_changed():
	result = subprocess.run('git diff --name-only HEAD^ HEAD', shell=True, capture_output=True, text=True)
	days = {}
	for line in result.stdout.split('\n'):
		m = re.search(r'aoc/day_(\d\d)', line)
		if m:
			days[m.group(1)] = True
	print(" ".join(days.keys()))

def days_completed():
	days = []
	for file in os.listdir('aoc'):
		if 'results' in file:
			days.append(file[4:6]) # day_[..].*
	return days

def print_outfile():
	out = '''<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Advent of Code 2023</title>
	<style>
	  @import url("https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@300");
	  body { margin:0;font-family:sans-serif;background-color:#303030;color:#e0e0e0 }
		h1, h2, h3, h4 { font-weight:400 }
		.doctitle { font-style:italic;font-size:2.4rem;line-height:3.8rem }
		.day h1 { font-size:1.8rem }
		.day { border:solid 1px gray;border-radius:1rem;padding:0.8rem }
		pre { background-color:#0f0f23;color:#cccccc;padding:0.8rem 1.2rem;border-radius:0.6rem }
		code { font-family:'Source Code Pro',monospace }
		main { margin:20px; }
		.my-solution { background-color:#464646;padding:0.4rem 0.8rem;border-radius:0.8rem }
	</style>
</head>
<body>
<main>
<h1 class="doctitle">The Advent of Code, 2023</h1>
'''
	import importlib, markdown
	days = days_completed()
	for day in days:
		day_n = importlib.import_module(f'..day_{day}', package='aoc.subpkg')
		out += '<article class="day">'
		out += markdown.markdown(day_n.__doc__)
		out += f'<div class="my-solution"><h2>Day {day} solution</h2>\n'
		out += f'<p><a href="https://github.com/arkadianriver/AoC-2023/blob/main/aoc/day_{day}.py">Link to the code</a>,'
		out += 'with these results:</p><pre><code>'
		with open(f'./aoc/day_{day}-results.txt', 'r') as f:
			out += f.read()
		out += '\n</code></pre></div>\n</article>\n'
	out += '</main></body></html>'
	with open('./out/index.html', 'w', encoding='utf-8') as of:
		of.write(out)
