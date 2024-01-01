import os, re
import subprocess

class Utils():

	def __init__(self, filename):
		self.filename = filename
		self.dp0 = os.path.dirname(os.path.realpath(filename))
		self.a_day = os.path.splitext(os.path.basename(filename))[0]
		self.inbase = f'{self.dp0}/{self.a_day}-input'

	def output(self, result):
		with open(f'{self.dp0}/{self.a_day}-results.txt', 'w', encoding='utf-8') as of:
			of.write(result)

def list_changed():
	result = subprocess.run('git diff --name-only HEAD^ HEAD', shell=True, capture_output=True, text=True)
	days = {}
	for line in result.stdout.split('\n'):
		m = re.search(r'aoc/(\d\d)', line)
		if m:
			days[m.group(1)] = True
	print(" ".join(days.keys()))

def days_completed():
	days = []
	for file in os.listdir('aoc'):
		if 'results' in file:
			days.append(file[:2])
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
		h1 { font-style:italic;font-weight:400;font-size:2.2rem;line-height:3.8rem }
		h2 { font-size:1.2rem }
		pre { background-color:#0f0f23;color:#cccccc;padding:1.2rem }
		code { font-family:'Source Code Pro',monospace }
		main { margin:20px; }
	</style>
</head>
<body>
<main>
<h1>The Advent of Code, 2023</h1>
'''
	days = days_completed()
	for day in days:
		out += f"<h2>Day {day}</h2>\n<pre><code>"
		with open(f'./aoc/{day}-results.txt', 'r') as f:
			out += f.read()
		out += '\n</code></pre>\n'
	out += '</main></body></html>'
	with open('./out/index.html', 'w', encoding='utf-8') as of:
		of.write(out)
