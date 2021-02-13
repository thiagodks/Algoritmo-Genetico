import numpy as np
import random
import math

class Individuo:
	
	def __init__(self, nbits=100, ndim=10, xmax=3, xmin=-3, fitness=999999, cromo_random=True):
		self.fitness = fitness
		self.nbits = nbits
		self.xmin = xmin
		self.xmax = xmax
		self.ndim = ndim
		self.cromossomo = list(np.random.randint(0,2, (self.nbits * self.ndim))) if cromo_random else [None] * (self.nbits * self.ndim)
		# print("cromossomo: ", self.cromossomo)

	def calc_fitness(self):
		self.fitness = self.func_obj(self.mapeamento())

	def chunks(self, lista, n):
		inicio = 0
		for i in range(n):
			final = inicio + len(lista[i::n])
			yield lista[inicio:final]
			inicio = final
	
	def mapeamento(self):
		splited = list(self.chunks(self.cromossomo, self.ndim))
		# print("cromossomo: ", self.cromossomo)
		# print("splited: ", splited)
		# print("ndim: ", self.ndim)
		self.x_ns = []
		for cromo_splited in splited:
			x_i = self.xmin + (((self.xmax - self.xmin)/((2 ** (self.nbits)) -1)) * self.bin_to_int(cromo_splited))
			self.x_ns.append(x_i)
		# print("x_ns: ", self.x_ns)
		# input("")
		return self.x_ns

	def bin_to_int(self, code_bin):
		result = int("".join(str(i) for i in code_bin),2)
		return result 

	def func_obj(self, x):
		n = float(len(x))
		f_exp = -0.2 * math.sqrt(1/n * sum(np.power(x, 2)))
		t = 0
		for i in range(0, len(x)):
			t += np.cos(2 * math.pi * x[i])
		s_exp = 1.0/n * t
		f = -20 * math.exp(f_exp) - math.exp(s_exp) + 20 + math.exp(1)
		return f

	def show_xns(self):
		string = ""
		for i, valor in enumerate(self.x_ns):
			string += "x"+str(i)+": %.7f" % valor + "\n"
		return string 
