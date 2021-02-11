import matplotlib.pyplot as plt
from individuo import Individuo
from populacao import Populacao
from termcolor import colored
from tqdm import tqdm
import numpy as np
import itertools
import pickle
import random 
import math
import time

def save_log_pop(populacao, nome):
	with open('solucoes/'+nome+'.pickle', 'wb') as fp:
		pickle.dump(populacao, fp)

def load_log_pop(name):
	with open('solucoes/'+name+'.pickle', 'rb') as fp:
		populacao = pickle.load(fp)
	return populacao

npop = [i for i in range(100, 500, 100)]
nger = [i for i in range(100, 500, 100)]
taxa_mutacao = [0.01, 0.05, 0.1, 0.15]
taxa_cruzamento = [0.6, 0.8, 1]
nbits = [i for i in range(2, 12, 2)]

print(npop, nger, taxa_cruzamento, taxa_mutacao, nbits)
all_list = [npop, nger, taxa_mutacao, taxa_cruzamento, nbits]
parametros = list(itertools.product(*all_list)) 

print("\n\nAlgoritmo Genético em execução...")

MELHOR_INDIVIDUO_GERAL = Individuo(fitness=999999, cromo_random=False)
PIOR_MELHOR_INDIVIDUO_GERAL = Individuo(fitness=-999999, cromo_random=False)
PIOR_INDIVIDUO_GERAL = Individuo(fitness=-999999, cromo_random=False)
NDIM = 5

for prmt in tqdm(parametros, position=0, leave=True):

	inicio = time.time()

	populacao = Populacao(npop=prmt[0], nger=prmt[1], elitismo=True)
	populacao.inicializa_indiv(taxa_mutacao=prmt[2], taxa_cruzamento=prmt[3], pv=0.9, nbits=prmt[4], ndim=NDIM, xmax=3, xmin=-3)
	# populacao = Populacao(npop=1000, nger=1000, elitismo=True)
	# populacao.inicializa_indiv(taxa_mutacao=0.05, taxa_cruzamento=0.8, pv=0.9, nbits=10, ndim=10, xmax=3, xmin=-3)
	populacao.print_parametros()

	for geracao_atual in tqdm(range(0, populacao.nger), position=0, leave=True):
		populacao.exec_ger()

	fim = time.time()
	log_fitness = list(map(list, zip(*populacao.log_fitness)))
	melhores_ger, piores_ger, media_ger = log_fitness[0], log_fitness[1], log_fitness[2]

	if populacao.melhor_individuo.fitness < MELHOR_INDIVIDUO_GERAL.fitness:
		MELHOR_INDIVIDUO_GERAL = populacao.melhor_individuo
		save_log_pop(populacao, "melhor_ndim="+str(NDIM))

	if populacao.melhor_individuo.fitness > PIOR_MELHOR_INDIVIDUO_GERAL.fitness:
		PIOR_MELHOR_INDIVIDUO_GERAL = populacao.melhor_individuo
		save_log_pop(populacao, "pior_melhor_ndim="+str(NDIM))

	if populacao.pior_individuo.fitness > PIOR_INDIVIDUO_GERAL.fitness:
		PIOR_INDIVIDUO_GERAL = populacao.pior_individuo
		save_log_pop(populacao, "pior_ndim="+str(NDIM))

	print(colored('\033[1m'+"\n-> Melhor Indivíduo: %.10f" % populacao.melhor_individuo.fitness, "green")) 
	print("Xns: ", populacao.melhor_individuo.x_ns)
	print(colored('\033[1m'+"\n-> Pior Indivíduo: %.10f" % populacao.pior_individuo.fitness, "red")) 
	print("Xns: ", populacao.pior_individuo.x_ns)
	print(colored('\033[1m'+"\n-> Melhor Indivíduo GERAL: %.10f" % MELHOR_INDIVIDUO_GERAL.fitness, "green")) 
	print("Xns: ", MELHOR_INDIVIDUO_GERAL.x_ns)
	print(colored('\033[1m'+"\n-> Pior Indivíduo GERAL: %.10f" % PIOR_INDIVIDUO_GERAL.fitness, "red")) 
	print("Xns: ", PIOR_INDIVIDUO_GERAL.x_ns)
	print(colored('\033[1m'+"\n-> Pior Melhor Indivíduo GERAL: %.10f" % PIOR_MELHOR_INDIVIDUO_GERAL.fitness, "red")) 
	print("Xns: ", PIOR_MELHOR_INDIVIDUO_GERAL.x_ns)
	print(colored('\033[1m'+"\n-> Media Fitness: %.10f" % np.mean(media_ger), "blue")) 
	print(colored('\033[1m'+"\n-> Tempo de execução: ", "green"), "%.4f" % (fim-inicio), "seg.\n")

###################################### PLOT GRAPHICS ############################################

pop_melhor = load_log_pop("melhor_ndim="+str(NDIM))
pop_pior = load_log_pop("pior_ndim="+str(NDIM))
pop_pior_melhor = load_log_pop("pior_melhor_ndim="+str(NDIM))
populacoes ={"melhor":pop_melhor, "pior": pop_pior, "pior_melhor": pop_pior_melhor}

for nome, populacao in populacoes.items():

	log_fitness = list(map(list, zip(*populacao.log_fitness)))
	melhores_ger, piores_ger, media_ger = log_fitness[0], log_fitness[1], log_fitness[2]

	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
	fig.set_size_inches(35, 20)
	title = fig.suptitle('Fitness - AG', fontsize=40, x=0.52)

	plt.rcParams.update({'font.size': 20})
	plt.gcf().text(0.01, 0.3, (populacao.parametros + 'Melhor Fitness: %.7f' % populacao.melhor_individuo.fitness +
					 '\n'+ populacao.melhor_individuo.show_xns() +
					 '\n\nPior Fitness: %.7f' % populacao.pior_individuo.fitness +
					 '\n' + populacao.pior_individuo.show_xns() +
					 '\n\nMedia Fitness: %.7f' % np.mean(media_ger)), fontsize=16)

	ax1.set_title("Melhores fitness a cada geração (1 a "+str(populacao.nger)+")")
	ax1.set_xlabel("Gerações", fontsize='medium')
	ax1.set_ylabel("Fitness", fontsize='medium')
	ax1.plot(list(range(0, populacao.nger)), melhores_ger[0:], 'g--', label='Melhor Fitness: %.7f' % populacao.melhor_individuo.fitness)
	ax1.legend(ncol=3)
	ax1.tick_params(labelsize=18)

	ax2.set_title("Melhores fitness a cada geração (10 a "+str(populacao.nger)+")")
	ax2.set_xlabel("Gerações", fontsize='medium')
	ax2.set_ylabel("Fitness", fontsize='medium')
	ax2.plot(list(range(10, populacao.nger)), melhores_ger[10:], 'g--', label='Melhor Fitness: %.7f' % populacao.melhor_individuo.fitness)
	ax2.legend(ncol=3)
	ax2.tick_params(labelsize=18)

	ax3.set_title("Piores fitness a cada geração")
	ax3.set_xlabel("Gerações", fontsize='medium')
	ax3.set_ylabel("Fitness", fontsize='medium')
	ax3.plot(list(range(0, populacao.nger)), piores_ger, 'r--', label='Pior Fitness: %.7f' % populacao.pior_individuo.fitness)
	ax3.legend(ncol=3)
	ax3.tick_params(labelsize=18)

	ax4.set_title("Media das fitness a cada geração")
	ax4.set_xlabel("Gerações", fontsize='medium')
	ax4.set_ylabel("Fitness", fontsize='medium')
	ax4.plot(list(range(0, populacao.nger)), media_ger, 'b--', label='Media Fitness: %.7f' % np.mean(media_ger))
	ax4.legend(ncol=3)
	ax4.tick_params(labelsize=18)

	plt.subplots_adjust(left=0.15)
	# fig.savefig('graficos/'+populacao.nome_arq+'fitness.png')
	fig.savefig('graficos/'+nome+"_"+populacao.nome_arq+'fitness.png')