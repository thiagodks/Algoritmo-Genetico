import matplotlib.pyplot as plt
import numpy as np
import pickle
 
def save_log_pop(populacao, nome):
	with open('solucoes/'+nome+populacao.nome_arq+'.pickle', 'wb') as fp:
		pickle.dump(populacao, fp)

def load_log_pop(name):
	with open('solucoes/'+name+'.pickle', 'rb') as fp:
		populacao = pickle.load(fp)
	return populacao

def plot_graphics(populacao, name_save=""):

	log_ger = list(map(list, zip(*populacao.log_ger)))
	melhores_ger, media_ger, mediana_ger, std_fitness = log_ger[0], log_ger[1], log_ger[2], log_ger[3]

	fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
	fig.set_size_inches(40, 11)
	title = fig.suptitle('Fitness - AG', fontsize=40, x=0.52, y=0.97)

	plt.rcParams.update({'font.size': 20})
	plt.subplots_adjust(left=0.15, top=0.85)
	plt.gcf().text(0.01, 0.25, (populacao.parametros + 'Melhor Fitness: %.7f' % populacao.melhor_individuo.fitness +
					 '\n'+ populacao.melhor_individuo.show_xns() +
					 '\n\nMedia Fitness: %.7f' % populacao.media_fitness +
					 '\n\nMediana Fitness: %.7f' % populacao.mediana_fitness +
					 '\n\nStd Fitness: %.7f' % populacao.std_fitness), fontsize=16)

	ax1.set_title("Melhores fitness a cada geração (1 a "+str(populacao.nger)+")")
	ax1.set_xlabel("Gerações", fontsize='medium')
	ax1.set_ylabel("Fitness", fontsize='medium')
	ax1.plot(list(range(0, populacao.nger)), melhores_ger, 'g--', label='Melhor Fitness: %.7f' % populacao.melhor_individuo.fitness)
	ax1.legend(ncol=3)
	ax1.tick_params(labelsize=18)

	ax2.set_title("Media e Mediana da fitness a cada geração")
	ax2.set_xlabel("Gerações", fontsize='medium')
	ax2.set_ylabel("Fitness", fontsize='medium')
	ax2.plot(list(range(0, populacao.nger)), media_ger, 'r--', label='Media Fitness: %.4f' % populacao.media_fitness)
	ax2.plot(list(range(0, populacao.nger)), mediana_ger, 'b--', label='Mediana Fitness: %.4f' % populacao.mediana_fitness)
	ax2.legend(ncol=1)
	ax2.tick_params(labelsize=18)

	ax3.set_title("Comparação entre as fitness a cada geração")
	ax3.set_xlabel("Gerações", fontsize='medium')
	ax3.set_ylabel("Fitness", fontsize='medium')
	ax3.plot(list(range(0, populacao.nger)), melhores_ger, 'g--', label='Melhor Fitness: %.4f' % populacao.melhor_individuo.fitness)
	ax3.plot(list(range(0, populacao.nger)), media_ger, 'r--', label='Media Fitness: %.4f' % populacao.media_fitness)
	ax3.plot(list(range(0, populacao.nger)), mediana_ger, 'b--', label='Mediana Fitness: %.4f' % populacao.mediana_fitness)
	ax3.legend(ncol=1)
	ax3.tick_params(labelsize=18)

	# plt.legend(bbox_to_anchor=(0.46, 0.8), ncol=1)
	fig.savefig('graficos/'+name_save+populacao.nome_arq+'fitness.png')
