import numpy as np
import matplotlib.pyplot as plt

def read_archive(directory, sep):

	file = open(directory, "r")
	result = []
	for row in file:
		values = row.split(sep)
		result.append([np.float(i) for i in values[:len(values)-1]])

	print(result)

	file.close()
	return result


def plot_graphics(melhores_ger=[], media_ger=[], mediana_ger=[], name_save=""):

	# melhores_ger, media_ger, mediana_ger, std_fitness = log_ger[0], log_ger[1], log_ger[2], log_ger[3]

	fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
	fig.set_size_inches(40, 11)
	title = fig.suptitle('Fitness - AG', fontsize=40, x=0.52, y=0.97)

	plt.rcParams.update({'font.size': 20})
	plt.subplots_adjust(left=0.15, top=0.85)


	#se quiser mudar o texto do lado do grafico, pq o meu tava cm base nas minhas classes python
	
	# plt.gcf().text(0.01, 0.25, (populacao.parametros + 'Melhor Fitness: %.7f' % populacao.melhor_individuo.fitness +
					 # '\n'+ populacao.melhor_individuo.show_xns() +
					 # '\n\nMedia Fitness: %.7f' % populacao.media_fitness +
					 # '\n\nMediana Fitness: %.7f' % populacao.mediana_fitness +
					 # '\n\nStd Fitness: %.7f' % populacao.std_fitness), fontsize=16)

	ax1.set_title("Melhores fitness a cada geração (1 a "+str(len(melhores_ger))+")")
	ax1.set_xlabel("Gerações", fontsize='medium')
	ax1.set_ylabel("Fitness", fontsize='medium')
	ax1.plot(list(range(0, len(melhores_ger))), melhores_ger, 'g--', label='Melhor Fitness: %.7f' % melhores_ger[-1])
	ax1.legend(ncol=3)
	ax1.tick_params(labelsize=18)

	ax2.set_title("Media e Mediana da fitness a cada geração")
	ax2.set_xlabel("Gerações", fontsize='medium')
	ax2.set_ylabel("Fitness", fontsize='medium')
	ax2.plot(list(range(0, len(melhores_ger))), media_ger, 'r--', label='Media Fitness: %.4f' % np.mean(media_ger))
	ax2.plot(list(range(0, len(melhores_ger))), mediana_ger, 'b--', label='Mediana Fitness: %.4f' % np.median(mediana_ger))
	ax2.legend(ncol=1)
	ax2.tick_params(labelsize=18)

	ax3.set_title("Comparação entre as fitness a cada geração")
	ax3.set_xlabel("Gerações", fontsize='medium')
	ax3.set_ylabel("Fitness", fontsize='medium')
	ax3.plot(list(range(0, len(melhores_ger))), melhores_ger, 'g--', label='Melhor Fitness: %.4f' % melhores_ger[-1])
	ax3.plot(list(range(0, len(melhores_ger))), media_ger, 'r--', label='Media Fitness: %.4f' % np.mean(media_ger))
	ax3.plot(list(range(0, len(melhores_ger))), mediana_ger, 'b--', label='Mediana Fitness: %.4f' % np.median(mediana_ger))
	ax3.legend(ncol=1)
	ax3.tick_params(labelsize=18)

	# plt.legend(bbox_to_anchor=(0.46, 0.8), ncol=1)
	fig.savefig(name_save+'_fitness.png')

result = read_archive("fitness_throught_generation.log", ",")
# media_ger = read_archive("arquivo2", "separador")
# mediana_ger = read_archive("arquivo3", "separador")

plot_graphics(melhores_ger=result[0], media_ger=result[1], mediana_ger=result[2])