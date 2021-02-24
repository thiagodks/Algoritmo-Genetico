import numpy as np
import random
import math

class Individuo:
	def __init__(self, ndim, xmax, xmin, fitness, cromo_random, taxa_mutacao):
		self.fitness = fitness
		self.xmin = xmin
		self.xmax = xmax
		self.ndim = ndim
		self.taxa_mutacao = taxa_mutacao
		self.cromo_random = cromo_random

	def func_obj(self, x):
		n = float(len(x))
		f_exp = -0.2 * math.sqrt(1/n * sum(np.power(x, 2)))
		t = 0
		for i in range(0, len(x)):
			t += np.cos(2 * math.pi * x[i])
		s_exp = 1.0/n * t
		f = -20 * math.exp(f_exp) - math.exp(s_exp) + 20 + math.exp(1)
		return f

class Individuo_Bin(Individuo):
	
	def __init__(self, nbits=100, ndim=10, xmax=3, xmin=-3, fitness=999999, cromo_random=True, taxa_mutacao=0.05):
		super().__init__(ndim=ndim, xmax=xmax, xmin=xmin, fitness=fitness, cromo_random=cromo_random, taxa_mutacao=taxa_mutacao)
		self.nbits = nbits
		self.cromossomo = list(np.random.randint(0,2, (self.nbits * self.ndim))) if cromo_random else [None] * (self.nbits * self.ndim)

	def calc_fitness(self):
		self.fitness = self.func_obj(self.mapeamento())

	def exec_mutacao(self):
		for indice, gene in enumerate(self.cromossomo):
			if random.random() < self.taxa_mutacao:
				novo_gene = 1 if gene == 0 else 0
				self.cromossomo[indice] = novo_gene

	def chunks(self, lista, n):
		inicio = 0
		for i in range(n):
			final = inicio + len(lista[i::n])
			yield lista[inicio:final]
			inicio = final
	
	def mapeamento(self):
		splited = list(self.chunks(self.cromossomo, self.ndim))
		self.x_ns = []
		for cromo_splited in splited:
			x_i = self.xmin + (((self.xmax - self.xmin)/((2 ** (self.nbits)) -1)) * self.bin_to_int(cromo_splited))
			self.x_ns.append(x_i)
		return self.x_ns

	def bin_to_int(self, code_bin):
		result = int("".join(str(i) for i in code_bin),2)
		return result 

	def show_xns(self):
		string = ""
		for i, valor in enumerate(self.x_ns):
			string += "x"+str(i)+": %.7f" % valor + "\n"
		return string 


class Individuo_Real(Individuo):
	
	def __init__(self, ndim=10, xmax=3, xmin=-3, fitness=999999, cromo_random=True):
		super().__init__(ndim=ndim, xmax=xmax, xmin=xmin, fitness=fitness, cromo_random=True)
		self.cromossomo = [random.uniform(xmin, xmax) for _ in range(ndim)] if cromo_random else [None] * ndim

	def calc_fitness(self):
		self.fitness = self.func_obj(self.cromossomo)

	def exec_mutacao(self):
		pass
		# for indice, gene in enumerate(self.cromossomo):
		# 	if random.random() < self.taxa_mutacao:
		# 		novo_gene = 1 if gene == 0 else 0
		# 		self.cromossomo[indice] = novo_gene

	def show_xns(self):
		string = ""
		for i, valor in enumerate(self.cromossomo):
			string += "x"+str(i)+": %.7f" % valor + "\n"
		return string 
