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

args = sys.argv
combo = str(args[1])
type = int(args[2])

fig = plt.figure()


f = 'aa' + combo + '.dat'
f = open(f, 'r')

hist = []; viol = []; cos = []; loc = []

histx = []; violx = []; cosx = []; locx = []

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
	if combo[-1:] == 6:
		loc.append(6*6*100000)
	else:
		loc.append(8*8*100000)

	loc[0] = 1
	
	histx.append(hist)
	violx.append(viol[-1])
	cosx.append(cos[-1])
	print('main' + str(cos))
	print('loc' + str(loc))
	if type == 1:
		plt.plot(loc, hist, 'r-')
	elif type == 2:
		plt.plot(loc, viol, 'b-')
	else:
		plt.plot(loc, cos, 'g-')
		

if type == 1:
	plt.ylabel('Objective')
	plt.title(combo + '-Objective')
	s = './Lines/PTO_TTP_' + str(combo) + '_Objective' + '.pdf'
elif type == 2:
	plt.ylabel('violations')
	plt.title(combo + '-Violations')
	s = './Lines/PTO_TTP_' + str(combo) + '_Violations' + '.pdf'
else:
	plt.ylabel('Costs')	
	plt.title(combo + '-Costs')
	s = './Lines/PTO_TTP_' + str(combo) + '_Costs' + '.pdf'
plt.gcf().subplots_adjust(left=0.15)
plt.xlabel('Iterations')
plt.legend()

#plt.boxplot(histx)

plt.savefig(s)
#plt.show()

	
