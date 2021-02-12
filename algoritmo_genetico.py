from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
from individuo import Individuo
from populacao import Populacao
from termcolor import colored
import multiprocessing
from tqdm import tqdm
import numpy as np
import itertools
import pickle
import random 
import math
import time
import util
import os

def exec_ag(prmt):

	populacao = Populacao(npop=prmt[0], nger=prmt[1], elitismo=True)
	populacao.inicializa_indiv(taxa_mutacao=prmt[2], taxa_cruzamento=prmt[3], pv=0.9, nbits=prmt[4], ndim=NDIM, xmax=3, xmin=-3)

	for geracao_atual in range(0, populacao.nger):
		populacao.exec_ger()

	return populacao

EXEC_PARALELA = True

print("\n\nAlgoritmo Genético Paralelo em execução...")
if not EXEC_PARALELA:

	inicio = time.time()
	populacao = Populacao(npop=500, nger=100, elitismo=True, gerar_log_exec=False)
	populacao.inicializa_indiv(taxa_mutacao=0.05, taxa_cruzamento=0.8, pv=0.9, nbits=10, ndim=5, xmax=3, xmin=-3)
	print(populacao.parametros)

	for geracao_atual in tqdm(range(0, populacao.nger), position=0, leave=True):
		populacao.exec_ger()

	fim = time.time()
	log_ger = list(map(list, zip(*populacao.log_ger)))
	melhores_ger, media_ger, mediana_ger, std_fitness = log_ger[0], log_ger[1], log_ger[2], log_ger[3]

	print(colored('\033[1m'+"\n-> Solução Encontrada: ", "green")) 
	print(colored('\033[1m'+"\n-> Melhor Indivíduo: %.10f" % populacao.melhor_individuo.fitness, "green")) 
	print("Xns: ", populacao.melhor_individuo.x_ns)
	print(colored('\033[1m'+"\n-> Media Fitness : %.10f" % populacao.media_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> Media Fitness Geral: %.10f" % np.mean(media_ger), "blue")) 
	print(colored('\033[1m'+"\n-> Mediana Fitness : %.10f" % populacao.mediana_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> Mediana Fitness Geral: %.10f" % np.mean(mediana_ger), "blue")) 
	print(colored('\033[1m'+"\n-> STD Fitness : %.10f" % populacao.std_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> STD Fitness Geral: %.10f" % np.mean(std_fitness), "blue")) 
	print(colored('\033[1m'+"\n-> Tempo de execução: ", "green"), "%.4f" % (fim-inicio), "seg.\n")

	util.plot_graphics(populacao)

else:

	inicio = time.time()

	npop = [i for i in range(400, 500, 100)]
	nger = [i for i in range(400, 500, 100)]
	taxa_mutacao = [0.01, 0.05, 0.1, 0.15]
	# taxa_mutacao = [0.01]
	taxa_cruzamento = [0.6, 0.8, 1]
	nbits = [i for i in range(2, 12, 2)]

	# npop = [i for i in range(100, 500, 100)]
	# nger = [i for i in range(100, 500, 100)]
	# taxa_mutacao = [0.01, 0.05, 0.1, 0.15]
	# taxa_cruzamento = [0.6, 0.8, 1]
	# nbits = [i for i in range(2, 12, 2)]
	NDIM = 5

	# print(npop, nger, taxa_cruzamento, taxa_mutacao, nbits)
	all_list = [npop, nger, taxa_mutacao, taxa_cruzamento, nbits]
	parametros = list(itertools.product(*all_list)) 

	executor = ProcessPoolExecutor()
	num_args = len(parametros)
	chunksize = int(num_args/multiprocessing.cpu_count())

	results = [i for i in tqdm(executor.map(exec_ag, parametros),total=num_args)]
	melhor_solucao = results[0]
	pior_solucao = results[0]
	for populacao in results:
		if populacao.melhor_individuo.fitness < melhor_solucao.melhor_individuo.fitness:
			melhor_solucao = populacao
		if populacao.melhor_individuo.fitness > pior_solucao.melhor_individuo.fitness:
			pior_solucao = populacao

	util.plot_graphics(melhor_solucao, "melhor_solucao")
	util.plot_graphics(pior_solucao, "pior_solucao")
	util.save_log_pop(melhor_solucao, "melhor_solucao_ndim:"+str(NDIM)+"_")
	util.save_log_pop(pior_solucao, "pior_solucao_ndim:"+str(NDIM)+"_")

	print(colored('\033[1m'+"\n#####################################\n-> Melhor Solução Encontrada: ", "green"), end="")
	print(melhor_solucao.parametros)
	print(colored('\033[1m'+"-> Melhor Indivíduo: %.10f" % melhor_solucao.melhor_individuo.fitness, "green")) 
	print("Xns: ", melhor_solucao.melhor_individuo.x_ns)
	print(colored('\033[1m'+"\n-> Media Fitness : %.10f" % melhor_solucao.media_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> Mediana Fitness : %.10f" % melhor_solucao.mediana_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> STD Fitness : %.10f" % melhor_solucao.std_fitness, "blue")) 

	print(colored('\033[1m'+"\n#####################################\n-> Pior Solução Encontrada: ", "red"), end="") 
	print(pior_solucao.parametros)
	print(colored('\033[1m'+"-> Melhor Indivíduo: %.10f" % pior_solucao.melhor_individuo.fitness, "green")) 
	print("Xns: ", pior_solucao.melhor_individuo.x_ns)
	print(colored('\033[1m'+"\n-> Media Fitness : %.10f" % pior_solucao.media_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> Mediana Fitness : %.10f" % pior_solucao.mediana_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> STD Fitness : %.10f" % pior_solucao.std_fitness, "blue")) 

	fim = time.time()
	print(colored('\033[1m'+"\n-> Tempo de execução: ", "green"), "%.4f" % (fim-inicio), "seg.\n")

	# for populacao in results:
	# 	print("parametros: ", populacao.parametros)
	# 	print("fitness: ", populacao.melhor_individuo.fitness, end="\n\n")