f=open('run_exp.sh', 'a')
for gen in range(1):
	for sol in range(1):
		for size in range(3):
			for seed in range(10):
				f.write('python test.py ' + str(sol) + ' ' + str(gen + 1) + ' ' + str(size) + ' ' + str(seed) + '\n')