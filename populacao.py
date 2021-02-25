from individuo import Individuo_Bin
from individuo import Individuo_Real
from termcolor import colored
import numpy as np
import itertools
import random
from util import trackcalls
import functools
import math

class Populacao:
	def __init__(self, tipo_rep='bin', selecao='torneio', cruzamento='ponto', npop=100, nger=200, 
				 elitismo=True, gerar_log_exec=False, taxa_cruzamento=0.7, pv=0.9):
		self.npop = npop
		self.nger = nger
		self.pv = pv
		self.log_ger = []
		self.taxa_cruzamento = taxa_cruzamento
		self.elitismo = elitismo
		self.gerar_log_exec = gerar_log_exec
		self.tipo_rep = tipo_rep
		self.selecao = selecao
		self.cruzamento = cruzamento

	def inicializa_indiv_bin(self, nbits=10, taxa_mutacao=0.05, ndim=10, xmax=3, xmin=-3):
		self.nbits = nbits
		self.ndim = ndim
		self.xmax = xmax
		self.xmin = xmin
		self.taxa_mutacao = taxa_mutacao
		self.individuos = [Individuo_Bin(nbits=nbits, ndim=ndim, xmax=xmax, xmin=xmin, taxa_mutacao=taxa_mutacao) for i in range(0, self.npop)]
		self.melhor_individuo = Individuo_Bin(nbits=nbits, ndim=ndim, xmax=xmax, xmin=xmin, cromo_random=False, taxa_mutacao=taxa_mutacao)
		self.pior_individuo = Individuo_Bin(nbits=nbits, ndim=ndim, xmax=xmax, xmin=xmin, fitness=-999999, cromo_random=False, taxa_mutacao=taxa_mutacao)
		self.nome_arq = ("BIN_npop:"+str(self.npop)+"_nger:"+str(self.nger)+"_nbits:"+str(nbits)+"_tm:"+str(self.taxa_mutacao)+
						"_xmin:"+str(self.xmin)+"_xmax:"+str(self.xmax)+"_ndim:"+str(self.ndim)+"_tc:"+str(self.taxa_cruzamento)+"_elitismo:"+str(self.elitismo)+"_")
		self.parametros = self.get_parametros()

	def inicializa_indiv_real(self, alpha=0.75, beta=0.25, taxa_mutacao=0.05, ndim=10, xmax=3, xmin=-3):
		self.alpha = alpha
		self.beta = beta
		self.ndim = ndim
		self.xmax = xmax
		self.xmin = xmin
		self.taxa_mutacao = taxa_mutacao
		self.individuos = [Individuo_Real(ndim=ndim, xmax=xmax, xmin=xmin, taxa_mutacao=taxa_mutacao) for i in range(0, self.npop)]
		self.melhor_individuo = Individuo_Real(ndim=ndim, xmax=xmax, xmin=xmin, cromo_random=False, taxa_mutacao=taxa_mutacao)
		self.pior_individuo = Individuo_Real(ndim=ndim, xmax=xmax, xmin=xmin, fitness=-999999, cromo_random=False, taxa_mutacao=taxa_mutacao)
		self.nome_arq = ("REAL_npop:"+str(self.npop)+"_nger:"+str(self.nger)+"_tm:"+str(taxa_mutacao)+
						"_xmin:"+str(xmin)+"_xmax:"+str(xmax)+"_ndim:"+str(ndim)+"_tc:"+str(self.taxa_cruzamento)+"_elitismo:"+str(self.elitismo)+"_")
		self.parametros = self.get_parametros()

	def avalia_pop(self):
		for i in range(0, len(self.individuos)):
			self.individuos[i].calc_fitness()

	def exec_cruzamento(self):
		if self.cruzamento == "ponto":
			self.cruzamento_ponto()
		elif self.cruzamento == "alpha_beta":
			self.cruzamento_alpha_beta()

	def exec_selecao(self):
		if self.selecao == "torneio":
			self.torneio()
		elif self.selecao == "roleta":
			self.roleta()

	@trackcalls
	def roleta(self):
		num_pais = 1
		self.pais = []
		total_fitness = 0
		individuos_fitness = []

		for i in range(0, len(self.individuos)):
			individuos_fitness.append(1/self.individuos[i].fitness)
			total_fitness += individuos_fitness[i]

		roleta_fitness = [individuos_fitness[i]/total_fitness for i in range(0, len(self.individuos))]
		while num_pais <= self.npop:
			r = random.random()
			soma = 0
			for j, valor in enumerate(roleta_fitness):
				soma += valor
				if soma >= r:
					self.pais.append(self.individuos[j])
					break
			num_pais += 1

	@trackcalls
	def torneio(self):
		self.pais = []
		num_pais = 1
		vencedor = None
		
		while num_pais <= self.npop:
		
			p1 = np.random.randint(0, self.npop)
			p2 = np.random.randint(0, self.npop)
		
			while p1 == p2:
				p2 = np.random.randint(0, self.npop)
		
			if(self.individuos[p2].fitness > self.individuos[p1].fitness):
				vencedor = self.individuos[p1] if random.random() < self.pv else self.individuos[p2]
			else:
				vencedor = self.individuos[p2] if random.random() < self.pv else self.individuos[p1]
			
			self.pais.append(vencedor)
			num_pais += 1

	@trackcalls
	def cruzamento_alpha_beta(self):
		self.individuos_interm = [Individuo_Real(ndim=self.ndim, xmax=self.xmax, xmin=self.xmin, cromo_random=False,
								  taxa_mutacao=self.taxa_mutacao) for i in range(0, self.npop)]
		self.num_individuos = 0
		cont = 0
		for i in range(0, len(self.pais), 2):

			if random.random() < self.taxa_cruzamento:

				if self.pais[i].fitness > self.pais[i+1].fitness:
					aux = self.pais[i+1]
					self.pais[i+1] = self.pais[i]
					self.pais[i] = aux

				for j in range(0, self.ndim):
					
					dj = np.abs(self.pais[i].cromossomo[j] - self.pais[i+1].cromossomo[j])
					
					if self.pais[i].cromossomo[j] <= self.pais[i+1].cromossomo[j]:
						u1 = random.uniform(self.pais[i].cromossomo[j] - self.alpha * dj, self.pais[i+1].cromossomo[j] + self.beta * dj)
						u2 = random.uniform(self.pais[i].cromossomo[j] - self.alpha * dj, self.pais[i+1].cromossomo[j] + self.beta * dj)
					else:
						u1 = random.uniform(self.pais[i+1].cromossomo[j] - self.alpha * dj, self.pais[i].cromossomo[j] + self.beta * dj)
						u2 = random.uniform(self.pais[i+1].cromossomo[j] - self.alpha * dj, self.pais[i].cromossomo[j] + self.beta * dj)
					
					u1 = u1 if not u1 < self.xmin else self.xmin
					u1 = u1 if not u1 > self.xmax else self.xmax
					u2 = u2 if not u2 < self.xmin else self.xmin
					u2 = u2 if not u2 > self.xmax else self.xmax
					
					self.individuos_interm[cont].cromossomo[j] = u1
					self.individuos_interm[cont+1].cromossomo[j] = u2
				
				self.individuos_interm[cont].exec_mutacao()
				self.individuos_interm[cont+1].exec_mutacao()
				
				self.num_individuos += 2
				cont += 2

	@trackcalls
	def cruzamento_ponto(self):
		cont = 0
		self.num_individuos = 0

		if self.tipo_rep == "bin":
			range_corte = self.nbits * self.ndim
			self.individuos_interm = [Individuo_Bin(nbits=self.nbits, ndim=self.ndim, xmax=self.xmax,
								 xmin=self.xmin, cromo_random=False, taxa_mutacao=self.taxa_mutacao) for i in range(0, self.npop)]
		else:
			range_corte = self.ndim
			self.individuos_interm = [Individuo_Real(ndim=self.ndim, xmax=self.xmax, xmin=self.xmin, cromo_random=False,
								  taxa_mutacao=self.taxa_mutacao) for i in range(0, self.npop)]
		
		for i in range(0, len(self.pais), 2):

			if random.random() < self.taxa_cruzamento:
				corte = random.randint(1,(range_corte) - 2)
				
				self.individuos_interm[cont].cromossomo = self.pais[i].cromossomo[:corte] + self.pais[i+1].cromossomo[corte:]
				self.individuos_interm[cont+1].cromossomo = self.pais[i+1].cromossomo[:corte] + self.pais[i].cromossomo[corte:]
				
				self.individuos_interm[cont].exec_mutacao()
				self.individuos_interm[cont+1].exec_mutacao()
				self.num_individuos += 2
				cont += 2

	def calc_log_ger(self):
		if self.tipo_rep == "bin":
			self.melhor_individuo = Individuo_Bin(nbits=self.nbits, ndim=self.ndim, xmax=self.xmax,
								 xmin=self.xmin, cromo_random=False, taxa_mutacao=self.taxa_mutacao)
		else:
			self.melhor_individuo = Individuo_Real(ndim=self.ndim, xmax=self.xmax, xmin=self.xmin, cromo_random=False,
								  taxa_mutacao=self.taxa_mutacao)
		self.media_fitness = []
		self.mediana_fitness = []
		self.std_fitness = []

		for individuo in self.individuos:
			if individuo.fitness < self.melhor_individuo.fitness:
				self.melhor_individuo = individuo

			self.media_fitness.append(individuo.fitness)
			self.mediana_fitness.append(individuo.fitness)
			self.std_fitness.append(individuo.fitness)

		self.media_fitness = np.mean(self.media_fitness)
		self.mediana_fitness = np.median(self.mediana_fitness)
		self.std_fitness = np.std(self.std_fitness)

		if self.gerar_log_exec:
			print(colored("\n\nMELHOR Individuo: ", "green"), self.melhor_individuo.fitness)
			if tipo_rep == "real": print(colored("Xns: ", "green"), self.melhor_individuo.cromossomo)
			else: print(colored("Xns: ", "green"), self.melhor_individuo.x_ns)
			print(colored("\nMEDIA fitness: ", "blue"), self.media_fitness)
			print(colored("\nMEDIANA fitness: ", "blue"), self.mediana_fitness)
			print(colored("\nSTD fitness: ", "blue"), self.std_fitness)
			self.print_pop(self.individuos, "Populacao atual: ")
		
		self.log_ger.append((self.melhor_individuo.fitness, self.media_fitness, self.mediana_fitness, self.std_fitness))
	
	def exec_elitismo(self):
		self.individuos[np.random.randint(0, self.npop)] = self.melhor_individuo

	def subst_pop(self):
		indices_disponiveis = [i for i in range(0, self.npop)]
		for novo_indv in range(0, self.num_individuos):
			indice_subst = random.choice(indices_disponiveis)
			self.individuos[indice_subst] = self.individuos_interm[novo_indv]
			indices_disponiveis.remove(indice_subst) 

	def print_pop(self, individuos, titulo=""):
		print("\n", titulo)
		for individuo in individuos:
			if individuo.fitness == self.pior_individuo.fitness: 
				print(colored("%.4f" % individuo.fitness, "red"), end=' | ')
			elif individuo.fitness == self.melhor_individuo.fitness: 
				print(colored("%.4f" % individuo.fitness, "green"), end=' | ')
			else:
				print("%.4f" % individuo.fitness, end=' | ')
		input("")

	def get_parametros(self):
		
		selecao, cruzam = "", ""
		if self.torneio.has_been_called: selecao = "\nMétodo de seleção: Torneio"
		elif self.roleta.has_been_called: selecao = "\nMétodo de seleção: Roleta"
		if self.cruzamento_ponto.has_been_called: cruzam = "\nMétodo de Cruzamento: Pontos"
		elif self.cruzamento_alpha_beta.has_been_called: cruzam = "\nMétodo de Cruzamento: Alpha Beta"
		
		if self.tipo_rep == 'bin':
			desc = ("\nNumero de bits: " + str(self.melhor_individuo.nbits) +
				   "\nTotal de bits (Indivíduo): " + str(self.melhor_individuo.ndim * self.melhor_individuo.nbits))
		else: 
			desc = ("\nAlpha: " + str(self.alpha) +
				   "\nBeta: " + str(self.beta))

		return (selecao + cruzam +
		"\nElitismo: " + str(self.elitismo) +
		"\nNúmero de Individuos: " + str(self.npop) +
		"\nNúmero de Gerações: " + str(self.nger) +
		"\nTaxa de Mutação: " + str(self.taxa_mutacao) +
		"\nTaxa de Cruzamento: " + str(self.taxa_cruzamento) +
		"\nProbabilidade do Vencedor: " + str(self.pv) + desc +
		"\nNumero de dimensões: " + str(self.melhor_individuo.ndim) +
		"\nxmax & xmin: " + str(self.melhor_individuo.xmin) +" & "+ str(self.melhor_individuo.xmax) + '\n')
