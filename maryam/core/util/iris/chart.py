"""
OWASP Maryam!
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


class main:

	def __init__(self):
		""" show histogram plot of web term frequency """
		self.framework = main.framework

	def line_chart(vectors, title, xlabel, ylabel, **args):
		import matplotlib.pyplot as plt

		for vector in vectors:
			x = [i for i in range(len(vector))]
			plt.plot(x, vector, **args)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)
		plt.legend()
		plt.show()

	def scatter_chart(vectors, title, xlabel, ylabel, **args):
		import matplotlib.pyplot as plt

		for vector in vectors:
			plt.scatter(vector[0], vector[1], **args)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)
		plt.legend()
		plt.show()
