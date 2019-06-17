import matplotlib.pyplot as plt
import numpy as np

#f = open('./HC4.dat', 'r')
a = open('./aaEAstart2_8.dat', 'a')
m = np.array([])
s = np.array([])
mn = np.array([])
mx = np.array([])
sols = []
endv = []
endc = []
a.write('aEAstart2_8_data	')
for j in range(2): # generator
	for k in range(2): # solver
		for l in range(2): # teamsize
			for i in range(10):
				if j == 0:
					sol = 'HC'
				else:
					sol = 'EA'
				if k == 0:
					gen = 'start1'
				else:
					gen = 'start2'
				if l == 0:
					team = '6'
				else:
					team = '8'
				if j == 1 and k == 1:
					f = 'a' + sol + gen + '-' + team + '_' + str(i) + '.dat'
				else:
					f = 'a' + sol + gen + '_' + team + '_' + str(i) + '.dat'
				if j == 1 and k == 0 and l == 1:
					f = sol + gen + '_' + team + '_' + str(i) + '.dat'
				a = './aa' + sol + gen + '_' + team + '.dat'
				f = open(f, 'r')
				a = open(a, 'a')
				hist = []
				viol = []
				cos = []
				line = f.readline()
				
				generator, solver, teamSize, runNo, budjet, solution, fitness, history, violations, costs = line.split('	')


				history = history.split(',')
				violations = violations.split(',')
				costs = costs.split(',')
				history[-1].strip('\n')
				#print(int(history[1]))


				counter = 0
				hpos = 0
				bestHist = -float(history[1])
				locations = []
				for item in history:
					#print(item)
					if item != history[0] and item != history[-1]:
						item = item.replace(',', '')
						if abs(float(item)) == abs(float(fitness)):
							if hpos == 0:
								hpos = counter
						if -float(item) < bestHist:
							hist.append(-float(item))
							locations.append(counter)
							bestHist = -float(item)
						#print('n')
						counter+=1
	
				for item in locations:
					viol.append(-float(violations[item]))
					cos.append(-float(costs[item]))	
				a.write(str(hist))
				a.write('	')
				a.write(str(viol))
				a.write('	')
				a.write(str(cos))
				a.write('	')
				a.write(str(locations))
				a.write('\n')


	#print(len(hist))
	#print(locations)
	#for item in costs:
	#	#print(item)
	#	if item != costs[0] and item != costs[-1]:
	#		item = item.replace(',', '')
	#		#print(item)
	#		
	#		cos.append(-float(item))
	#		#print('n')
	#	
	#for item in violations:
	#	#print(item)
	#	if item != violations[0] and item != violations[-1]:
	#		item = item.replace(',', '')
	#		#print(item)
	#		viol.append(-float(item))
	#		#print('n')
	
	
		

#	vm = np.mean(viol)
#	vs = np.std(viol)
#	vmn = np.min(viol)
#	vmx = np.max(viol)
#	
#	cm = np.mean(cos)
#	cs = np.std(cos)
#	cmn = np.min(cos)
#	cmx = np.max(cos)
#
#	hm = np.mean(hist)
#	hs = np.std(hist)
#	hmn = np.min(hist)
#	hmx = np.max(hist)
	
##	a.write(str(vm))	
#	a.write('	')
#	a.write(str(vs))
#	a.write('	')
#	a.write(str(vmn))
#	a.write('	')
#	a.write(str(vmx))
#	a.write('	')
#	a.write('\n')
#	
#	a.write(str(cm))	
#	a.write('	')
#	a.write(str(cs))
#	a.write('	')
#	a.write(str(cmn))
#	a.write('	')
#	a.write(str(cmx))
#	a.write('	')
#	a.write('\n')
#	
#	a.write(str(hm))	
#	a.write('	')
#	a.write(str(hs))
#	a.write('	')
#	a.write(str(hmn))
#	a.write('	')
#	a.write(str(hmx))
#	a.write('	')
#	a.write('\n')
	
	#print(vm, vs, vmn, vmx)
	#print(cm, cs, cmn, cmx)
	#print(hm, hs, hmn, hmx)
	#print(solution)
	
	#print(hpos)
	#print(hmx)
	
	#	sols.append(hist[-1])
#	endv.append(cos[-1])
#	endc.append(viol[-1])

#fig = plt.figure()
#ax = plt.axes()
#fig2 = plt.figure()
#ax2 = plt.axes()
#fig3 = plt.figure()
#ax3 = plt.axes()



#ax.boxplot(sols)
#ax2.boxplot(endv)
#ax3.boxplot(endc)
##ax.plot(cos)
#plt.show()
f.close()