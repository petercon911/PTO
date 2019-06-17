import matplotlib.pyplot as plt
import numpy as np
import sys

def parse(a):
	temp = []
	lin = a.split(',')
	for item in lin:
		item = item.strip('[')
		item = item.strip(']')
		item = item.strip('-')
		item = item.strip(',')
		item = item.strip(']\n')

		#print(item)
	
		temp.append(float(item))
	return temp




for tsize in range(2):
	hist = []; viol = []; cos = []; loc = []

	histx = []; violx = []; cosx = []; locx = []

	for size in range(4):
		if size == 0:
			f = 'aaHCstart1_' + str((tsize*2) + 6) + '.dat'
			f = open(f, 'r')
		elif size == 1:
			f = 'aaHCstart2_' + str((tsize*2) + 6) + '.dat'
			f = open(f, 'r')
		elif size == 2:
			f = 'aaEAstart1_' + str((tsize*2) + 6) + '.dat'
			f = open(f, 'r')
		else:
			f = 'aaEAstart2_' + str((tsize*2) + 6) + '.dat'
			f = open(f, 'r')
		
		for i in range(10):
			line = f.readline()
			print(line)
			line = line.split("	")
	
			hist = parse(line[0])
	
			for item in range(len(hist)):
				hist[item] = -hist[item]
	
	
			viol = parse(line[1])
			cos = parse(line[2])
			loc = parse(line[3])
	
			hist.append(hist[-1])
			viol.append(viol[-1])
			viol[0] = -viol[0]
			cos.append(cos[-1])
			cos[0] = -cos[0]
			loc.append(6*6*100000)
			loc[0] = 1
	
			histx.append(hist[-1])
			violx.append(viol[-1])
			cosx.append(cos[-1])
	#print('main' + str(cos))
	#print('loc' + str(loc))

	histx = np.array(histx)
	violx = np.array(violx)
	cosx = np.array(cosx)

	x1 = histx[:9]; x2 = histx[10:19]
	print(x1); print(x2)
	x = np.array((histx[:9], histx[10:19], histx[20:29], histx[30:39])).T
	plt.boxplot(x)
	plt.ylabel('Objective')
	plt.xlabel('Solver/Generators')
	plt.gcf().subplots_adjust(left=0.15)

	if tsize == 0:
		plt.title('Best Fitness - Team Size 6')
		s = './BoxPlot/PTO_TTP_Fitness_size6.pdf'
	if tsize == 1:
		plt.title('Best Fitness - Team Size 8')
		s = './BoxPlot/PTO_TTP_Fitness_size8.pdf'
	
	index = np.arange(4)
	bar_width = 1
	plt.xticks(index + bar_width, ('HC/1', 'HC/2', 'EA/1', 'EA/2'))
	plt.legend()

#plt.boxplot(histx)

	plt.savefig(s)
	
	plt.show()

