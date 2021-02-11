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

def save_log_pop(populacao):
	with open('solucoes/'+populacao.nome_arq+'.pickle', 'wb') as fp:
		pickle.dump(populacao, fp)

def load_log_pop(populacao, name):
	with open('solucoes/'+name, 'rb') as fp:
		populacao = pickle.load(fp)

print("\n\nAlgoritmo Genético em execução...")

inicio = time.time()

populacao = Populacao(npop=1000, nger=500, elitismo=False)
populacao.inicializa_indiv(taxa_mutacao=0.05, taxa_cruzamento=0.7, pv=0.9, nbits=10, ndim=10, xmax=3, xmin=-3)
populacao.print_parametros()

geracao_atual = 1
for geracao_atual in tqdm(range(0, populacao.nger), position=0, leave=True):
	populacao.run()
	geracao_atual += 1

fim = time.time()
log_fitness = list(map(list, zip(*populacao.log_fitness)))
melhores_ger, piores_ger, media_ger = log_fitness[0], log_fitness[1], log_fitness[2]

print(colored('\033[1m'+"\n-> Melhor Indivíduo: %.10f" % populacao.melhor_individuo.fitness, "green")) 
print("Xns: ", populacao.melhor_individuo.x_ns)
print(colored('\033[1m'+"\n-> Pior Indivíduo: %.10f" % populacao.pior_individuo.fitness, "red")) 
print("Xns: ", populacao.pior_individuo.x_ns)
print(colored('\033[1m'+"\n-> Media Fitness: %.10f" % np.mean(media_ger), "blue")) 
print(colored('\033[1m'+"\n-> Tempo de execução: ", "green"), "%.4f" % (fim-inicio), "seg.\n")

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
fig.savefig('graficos/'+populacao.nome_arq+'fitness.png')
save_log_pop(populacao)