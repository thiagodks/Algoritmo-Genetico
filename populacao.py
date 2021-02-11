from individuo import Individuo
from termcolor import colored
import numpy as np
import itertools
import random
import math

GENERATION_LOG = False

class Populacao:
	def __init__(self, npop=100, nger=200, elitismo=True):
		self.npop = npop
		self.nger = nger
		self.log_fitness = []
		self.elitismo = elitismo

	def inicializa_indiv(self, taxa_mutacao=0.05, taxa_cruzamento=0.7, pv=0.9, nbits=10, ndim=10, xmax=3, xmin=-3):
		self.pv = pv
		self.nbits = nbits
		self.ndim = ndim
		self.taxa_mutacao = taxa_mutacao
		self.taxa_cruzamento = taxa_cruzamento
		self.individuos = [Individuo(nbits=nbits, ndim=ndim, xmax=xmax, xmin=xmin) for i in range(0, self.npop)]
		self.melhor_individuo = Individuo(nbits=nbits, ndim=ndim, xmax=xmax, xmin=xmin, cromo_random=False)
		self.pior_individuo = Individuo(nbits=nbits, ndim=ndim, xmax=xmax, xmin=xmin, fitness=-999999, cromo_random=False)
		self.nome_arq = ("npop:"+str(self.npop)+"_nger:"+str(self.nger)+"_nbits:"+str(nbits)+"_tm:"+str(taxa_mutacao)+
						"_xmin:"+str(xmin)+"_xmax:"+str(xmax)+"_ndim:"+str(ndim)+"_tc:"+str(taxa_cruzamento)+"_elitismo:"+str(self.elitismo)+"_")

	def avalia_pop(self):
		for i in range(0, len(self.individuos)):
			self.individuos[i].calc_fitness()

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

	def cruzamento(self):
		self.individuos_interm = [Individuo(cromo_random=False) for i in range(0, self.npop)]
		self.num_individuos = 0
		cont = 0
		for i in range(0, len(self.pais), 2):

			if random.random() < self.taxa_cruzamento:
				corte = random.randint(1,(self.nbits * self.ndim) - 2)
				
				self.individuos_interm[cont].cromossomo = self.pais[i].cromossomo[:corte] + self.pais[i+1].cromossomo[corte:]
				self.individuos_interm[cont+1].cromossomo = self.pais[i+1].cromossomo[:corte] + self.pais[i].cromossomo[corte:]
				
				self.individuos_interm[cont] = self.mutacao(self.individuos_interm[cont])
				self.individuos_interm[cont+1] = self.mutacao(self.individuos_interm[cont+1])
				self.num_individuos += 2
				cont += 2

	def mutacao(self, individuo):
		for indice, gene in enumerate(individuo.cromossomo):
			if random.random() < self.taxa_mutacao:
				novo_gene = 1 if gene == 0 else 0
				individuo.cromossomo[indice] = novo_gene

		return individuo

	def calc_log_fitness(self):
		self.melhor_individuo = Individuo(nbits=self.nbits, cromo_random=False)
		pior_individuo_ger = Individuo(nbits=self.nbits, fitness=-999999, cromo_random=False)
		self.media_fitness = 0

		for individuo in self.individuos:
			if individuo.fitness < self.melhor_individuo.fitness:
				self.melhor_individuo = individuo
			if individuo.fitness > pior_individuo_ger.fitness:
				pior_individuo_ger = individuo

			self.media_fitness += individuo.fitness

		self.media_fitness /= len(self.individuos)
		
		if pior_individuo_ger.fitness > self.pior_individuo.fitness:
			self.pior_individuo = pior_individuo_ger

		if GENERATION_LOG:
			print(colored("\n\nMELHOR Individuo: ", "green"), self.melhor_individuo.fitness)
			print(colored("Xns: ", "green"), self.melhor_individuo.x_ns)
			print(colored("\nPIOR Individuo: ", "red"), pior_individuo_ger.fitness)
			print(colored("Xns: ", "red"), pior_individuo_ger.x_ns)
			print(colored("\nMEDIA fitness: ", "blue"), self.media_fitness)
			self.print_pop(self.individuos, "Populacao atual: ")
		
		self.log_fitness.append((self.melhor_individuo.fitness, pior_individuo_ger.fitness, self.media_fitness))
	
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

	def print_parametros(self):
		self.parametros = ("\n\nNúmero de Individuos: " + str(self.npop) +
		"\nNúmero de Gerações: " + str(self.nger) +
		"\nElitismo: " + str(self.elitismo) +
		"\nTaxa de Mutação: " + str(self.taxa_mutacao) +
		"\nTaxa de Cruzamento: " + str(self.taxa_cruzamento) +
		"\nProbabilidade do Vencedor: " + str(self.pv) +
		"\nNumero de bits: " + str(self.melhor_individuo.nbits) +
		"\nNumero de dimensões: " + str(self.melhor_individuo.ndim) +
		"\nTotal de bits (Indivíduo): " + str(self.melhor_individuo.ndim * self.melhor_individuo.nbits) +
		"\nxmax & xmin: " + str(self.melhor_individuo.xmin) +" & "+ str(self.melhor_individuo.xmax) + '\n\n')
		print('\033[1m' + colored(self.parametros, "green") + '\033[0m')

	def run(self):
		self.avalia_pop()
		self.torneio()
		self.cruzamento()
		self.calc_log_fitness()
		self.subst_pop()
		if self.elitismo: self.exec_elitismo()