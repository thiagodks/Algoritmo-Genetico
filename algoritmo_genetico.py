from concurrent.futures import ProcessPoolExecutor
from individuo import Individuo
from populacao import Populacao
from termcolor import colored
import multiprocessing
from tqdm import tqdm
import numpy as np
import itertools
import time
import util
import sys

def exec_ag(prmt):
	
	populacao = Populacao(tipo_rep='real', selecao='roleta', cruzamento='alpha_beta', npop=prmt[0], nger=prmt[1], elitismo=prmt[5], gerar_log_exec=False, taxa_cruzamento=prmt[3], pv=0.9)
	
	if populacao.tipo_rep == 'real': populacao.inicializa_indiv_real(alpha=0.75, beta=0.25, taxa_mutacao=prmt[2], ndim=prmt[4], xmax=3, xmin=-3)
	else: populacao.inicializa_indiv_bin(nbits=prmt[5], ndim=prmt[4], taxa_mutacao=prmt[2], xmax=3, xmin=-3)

	for geracao_atual in range(0, populacao.nger):
		populacao.avalia_pop()
		populacao.exec_selecao()
		populacao.exec_cruzamento()
		populacao.calc_log_ger()
		populacao.subst_pop()
		if populacao.elitismo: populacao.exec_elitismo()

	return populacao

EXEC_PARALELA = int(sys.argv[1])

if not EXEC_PARALELA:

	inicio = time.time()
	print("\nAlgoritmo Genético em execução...")
	
	populacao = Populacao(tipo_rep='real', selecao='roleta', cruzamento='ponto', npop=100, nger=100, elitismo=True, gerar_log_exec=False, taxa_cruzamento=0.8, pv=0.9)
	
	if populacao.tipo_rep == 'real': populacao.inicializa_indiv_real(alpha=0.75, beta=0.25, taxa_mutacao=0.05, ndim=10, xmax=2, xmin=-2)
	else: populacao.inicializa_indiv_bin(nbits=10, taxa_mutacao=0.05, ndim=10, xmax=3, xmin=-3)
	
	print(colored('\033[1m' + populacao.parametros + '\033[0m', "green"))
	for geracao_atual in tqdm(range(0, populacao.nger), position=0, leave=True):
		populacao.avalia_pop()
		populacao.exec_selecao()
		populacao.exec_cruzamento()
		populacao.calc_log_ger()
		populacao.subst_pop()
		if populacao.elitismo: populacao.exec_elitismo()

	fim = time.time()
	log_ger = list(map(list, zip(*populacao.log_ger)))
	melhores_ger, media_ger, mediana_ger, std_fitness = log_ger[0], log_ger[1], log_ger[2], log_ger[3]

	print(colored('\033[1m'+"\n-> Solução Encontrada: ", "green")) 
	print(colored('\033[1m'+"\n-> Melhor Indivíduo: %.10f" % populacao.melhor_individuo.fitness, "green")) 
	if populacao.tipo_rep == "real": print(colored("Xns: ", "green"), populacao.melhor_individuo.cromossomo)
	else: print(colored("Xns: ", "green"), populacao.melhor_individuo.x_ns)
	print(colored('\033[1m'+"\n-> Media Fitness : %.10f" % populacao.media_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> Media Fitness Geral: %.10f" % np.mean(media_ger), "blue")) 
	print(colored('\033[1m'+"\n-> Mediana Fitness : %.10f" % populacao.mediana_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> Mediana Fitness Geral: %.10f" % np.mean(mediana_ger), "blue")) 
	print(colored('\033[1m'+"\n-> STD Fitness : %.10f" % populacao.std_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> STD Fitness Geral: %.10f" % np.mean(std_fitness), "blue")) 
	print(colored('\033[1m'+"\n-> Tempo de execução: ", "green"), "%.4f" % (fim-inicio), "seg.\n")

	util.plot_graphics(populacao)

else:

	print("\n\nAlgoritmo Genético Paralelo em execução...")
	inicio = time.time()

	npop = [24, 50, 100]
	nger = [24, 50, 100]
	taxa_mutacao = [0.01, 0.05, 0.1]
	taxa_cruzamento = [0.6, 0.8, 1]
	ndim = [2, 5, 10]
	nbits = [i for i in range(4, 12, 2)]
	elitismo = [True, False]

	# all_list = [npop, nger, taxa_mutacao, taxa_cruzamento, ndim, nbits, elitismo]
	all_list = [npop, nger, taxa_mutacao, taxa_cruzamento, ndim, elitismo]
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
	util.save_log_pop(melhor_solucao, "melhor_solucao_")
	util.save_log_pop(pior_solucao, "pior_solucao_")

	print(colored('\033[1m'+"\n#####################################\n-> Melhor Solução Encontrada: ", "green"), end="")
	print(melhor_solucao.parametros)
	print(colored('\033[1m'+"-> Melhor Indivíduo: %.10f" % melhor_solucao.melhor_individuo.fitness, "green")) 
	if melhor_solucao.tipo_rep == "real": print(colored("Xns: ", "green"), melhor_solucao.melhor_individuo.cromossomo)
	else: print(colored("Xns: ", "green"), melhor_solucao.melhor_individuo.x_ns)
	print(colored('\033[1m'+"\n-> Media Fitness : %.10f" % melhor_solucao.media_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> Mediana Fitness : %.10f" % melhor_solucao.mediana_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> STD Fitness : %.10f" % melhor_solucao.std_fitness, "blue")) 

	print(colored('\033[1m'+"\n#####################################\n-> Pior Solução Encontrada: ", "red"), end="") 
	print(pior_solucao.get_parametros())
	print(colored('\033[1m'+"-> Melhor Indivíduo: %.10f" % pior_solucao.melhor_individuo.fitness, "green")) 
	if pior_solucao.tipo_rep == "real": print(colored("Xns: ", "green"), pior_solucao.melhor_individuo.cromossomo)
	else: print(colored("Xns: ", "green"), pior_solucao.melhor_individuo.x_ns)
	print(colored('\033[1m'+"\n-> Media Fitness : %.10f" % pior_solucao.media_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> Mediana Fitness : %.10f" % pior_solucao.mediana_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> STD Fitness : %.10f" % pior_solucao.std_fitness, "blue")) 

	fim = time.time()
	print(colored('\033[1m'+"\n-> Tempo de execução: ", "green"), "%.4f" % (fim-inicio), "seg.\n")