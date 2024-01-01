import os

class Utils():

	def __init__(self, filename):
		self.filename = filename
		self.dp0 = os.path.dirname(os.path.realpath(filename))
		self.a_day = os.path.splitext(os.path.basename(filename))[0]
		self.inbase = f'{self.dp0}/{self.a_day}-input'

	def output(self, result):
		with open(f'{self.dp0}/{self.a_day}-results.txt', 'w', encoding='utf-8') as of:
			of.write(result)
