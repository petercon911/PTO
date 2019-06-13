from PTO import random,random_function,solve, plot_runs, compare_all, make_table, stat_summary, plot_scalability
import math, time, pdb
import copy
#import matplotlib.pyplot as plt
import numpy as np
import sys
#random.seed(0)

def start1():
	S = np.array([[None for x in range(weeks)] for x in range(teams)])
	
	#S = randomPerm(S)
	S = randomPerm2(S) #for getGame2, currently error prone, trying number then removing
	#S = randomPerm3(S)	#for getGame3, works, creating list of available then random
	
	#print("end", S)
	#pdb.set_trace()

	return S
	

def start2():
	S = np.array([[None for x in range(weeks)] for x in range(teams)])
	
	#S = randomPerm(S)
	#S = randomPerm2(S) #for getGame2, currently error prone, trying number then removing
	S = randomPerm3(S)	#for getGame3, works, creating list of available then random
	
	#print("end", S)
	#pdb.set_trace()

	return S
	
	
#Not used
def randomPerm(S):
	for i in range(teams):
		for j in range(weeks):
			S[i][j] = getGame(i,j,S)
			#if temp > 0:
			#	S[abs(temp)-1][j] = - (i+1)
			#else:
			#	S[abs(temp)-1][j] =   (i+1)
			#S[i][j] = temp
	return S


#This generator is not used	
@random_function	
def getGame(x,y,S):
	easyR = [[None for x in range(weeks)] for x in range(teams)]
	for i in range(teams):
		easyR[i][y] = S[i][y] # building a T matrix of relevant possible violations
	
	for i in range(weeks):
		easyR[x][i] = S[x][i]
	
	
	# check both rows when putting in the opposite value
	# random jumps to check squares
	available = [x for x in range(-teams, teams + 1) if x != 0]
	#available = [x for x in available if x != 0]
	checkWeek = []
	checkTeam = []
	for week in easyR:
		checkWeek.append(week[y]) # reducing to 1D array of each week aka vertical
	for i in range(weeks):	
		checkTeam.append(easyR[x][i]) # each team , horizontal
	
	
	checkWeek = list(filter(lambda a: a != None, checkWeek))	# removing instances of None
	checkTeam = list(filter(lambda a: a != None, checkTeam))
	available = [k for k in available if abs(k) not in checkWeek and k not in checkTeam] # remove any duplicates
	available = [k for k in available if abs(k) != (x + 1)] # cant play yourself
	#print('t ', checkTeam, '  ', y)
	if checkTeam != []:
		#print(checkTeam[y-1])
		available = [k for k in available if abs(k) != abs(checkTeam[y-1])] #cannot play the team before again
	for i in range(len(checkWeek)):
		try:
			available.remove(i + 1) # needs to check for in in checkWeek, not the length range
		except:						# tries to remove double occurences in week, only 1-n in n teams
			print('y')
		try:
			available.remove(-(i + 1))
		except:
			print('z')
			
	#print('w ', checkWeek)
	#print('t ', checkTeam)
	#print('a ', available)
	#print(y)
	
	if len(checkTeam) > 2:
		if checkTeam[y-1] <0 and checkTeam[y-2] <0:
			available = [k for k in available if k > 0] # no repreat home or away
		if checkTeam[y-1] >0 and checkTeam[y-2] >0:
			available = [k for k in available if k < 0]
		if abs(checkTeam[y-1]) == abs(checkTeam[y-2]):
			available = [k for k in available if k != checkTeam[y-2]] # no consecutive games
#			print('t ', checkTeam)
		
	
	#available = [k for k in available if S[abs(k)-1][y] == None or S[abs(k)-1][y] == 0]
	
	
	if (x + 1) in checkWeek:
		rand = -(checkWeek.index(x+1) + 1) # fill in the opposite number for each selection
	elif -(x + 1) in checkWeek:
		rand = checkWeek.index(-(x+1)) + 1
	else:
		try:
			rand = random.choice(available)
		except:
			rand = 0
	
	return rand

	
#	for i in range(len(checkWeek)): checkWeek[i] = abs(checkWeek[i])
#
#	weekDup = [k for k,v in Counter(checkWeek).items() if v>1]	# creating array of duplicates over 1, essentially allowing 2 to exist
#	
#	
#	TeamDup = [k for k,v in Counter(checkTeam).items() if v>1]	# wont iterate list for some reason
#	print(checkTeam)
#	print(TeamDup)
#	
#	
#	
#	print(checkWeek)
#	print(weekDup)
#	
#	while rand in TeamDup:
#		rand = random.choice(range(1, teams))		# need to change to allow one home and away
#		
#		while rand in weekDup:
#			rand = random.choice(range(1, teams)) # no duplicate values over 2
#			
#			if rand in checkWeek and rand not in weekDup:					
#				rand = -rand		# home away marking
#			elif -rand in checkWeek:
#				print('x')
#				rand = random.choice(range(1, teams))	# already two instances of value, new value pick
#		while rand == x:
#			rand = random.choice(range(1, teams))	# cant play yourself
			
		
#	return rand
	
#Used to select the matrix tile
@random_function
def randomPerm3(S): # random pick of matrix square

	while not schedule_full(S):
		#print("HIIIIIIIIIIIIIIIIIIII")
		#print(S)
		#matrix = [[None for x in range(weeks)] for x in range(teams)] 
		spaceNone = []
		for team in range(teams):
			for week in range(weeks):
				if S[team][week] == None:
					spaceNone.append((team,week))
		#print('     AAA    ', spaceNone)
		if len(spaceNone) == 0:
			raise ValueError("HI")
		#print(S)
		#print(spaceNone)
		sp = spaceNone[:]
		x,y = random.choice(sp)
		#while S[x][y] != None:
		#	x = random.choice(range(teams))
		#	y = random.choice(range(weeks))
				
		if S[x][y] == None:
			temp = getGame3(x,y,S)
			S[x][y] = temp
			if temp != 0:
				if temp > 0:
					S[abs(temp)-1][y] = -(x + 1)
				else:
					S[abs(temp)-1][y] = x + 1
	
		
	return S

#Not used	
@random_function	
def randomPerm2(S):
	
	while not schedule_full(S):
		#print("HIIIIIIIIIIIIIIIIIIII")
		#print(S)
		#matrix = [[None for x in range(weeks)] for x in range(teams)] 
		spaceNone = []
		for team in range(teams):
			for week in range(weeks):
				if S[team][week] == None:
					spaceNone.append((team,week))
		#print('     AAA    ', spaceNone)
		
		sp = spaceNone[:]
		x,y = random.choice(sp)
		#while S[x][y] != None:
		#	x = random.choice(range(teams))
		#	y = random.choice(range(weeks))
				
		if S[x][y] == None:
			temp = getGame2(x,y,S)
			S[x][y] = temp
			if temp != 0:
				if temp > 0:
					S[abs(temp)-1][y] = -(x + 1)
				else:
					S[abs(temp)-1][y] = x + 1
	
		
	return S

#Works correctly at reducing available and then making random choice if available not 0
def getGame3(x,y,S):
	available = [i for i in range(-teams, teams + 1) if i != 0 and abs(i) != (x + 1)]
	
	a = []; b = [];
	for i in range(teams):
		a.append(S[i][y])
	#for i in range(weeks):
	#	b.append(S[x][i])
	
	b = S[x]
	
	available = [k for k in available if -k not in a and k not in a and k not in b] # remove any duplicates
	available = [k for k in available if abs(k) != (x + 1)] # cant play yourself
	
	if y > 2:
		if b[y-1] != None and b[y-2] != None and b[y-3] != None:
			if b[y-1] <0 and b[y-2] <0 and b[y-3] < 0:
				available = [k for k in available if k > 0] # no repreat home or away
			if b[y-1] >0 and b[y-2] >0 and b[y-3] >0:
				available = [k for k in available if k < 0]
			if abs(b[y-1]) == abs(b[y-2]):
				available = [k for k in available if k != b[y-2]] # no consecutive games
#				print('t ', b)
			
				#print(b[y-1])
			available = [k for k in available if abs(k) != (abs(b[y-1]))] #cannot play the team before again

			available = [k for k in available if S[(abs(k)-1)][y] != None]
	
	#trying to take cost matrix into account
	#if len(available) > 3:
	#	highest = 0
	#	marker = 0
	#	for k in available:
	#		temp = abs(costMat[x][y] - costMat[abs(k-1)][y])
	#		if temp > highest:
	#			highest = temp
	#			marker = k
	#	available.remove(k)
		
	if len(available) < 1:
		return 0
	else:
		return random.choice(available)
	
#Not working consistently, causes pop to appear empty in PTO
@random_function
def getGame2(x,y,S):
	# build available without 0 or the current team
	available = [i for i in range(-teams, teams + 1) if i != 0 and abs(i) != (x + 1)]
	rand = 00; 
	a = []; b = [];
	for i in range(teams):
		a.append(S[i][y])
	#for i in range(weeks):
	#	b.append(S[x][i])
	
	b = S[x]
	#print('A: ', available)
	#print(a)
	#print(b)
	av = available[:]
	
	while len(av): 
		
		
		rand = random.choice(av)
	#	print('RAND   ', rand)
		z = [];
		if S[(abs(rand) - 1)][y] == None or S[(abs(rand) - 1)][y] == 0: # opposite isn't full
			if rand > 0:
				opp = -(x+1)	# create opposite value
			else:
				opp = x + 1
			#for i in range(weeks):
			#	z.append(S[abs(rand)-1][i]) # create opposite row
				
			if valid(b,a,S[abs(rand)-1],rand,opp): 	# check if rand and opp are valid
				return rand
			
		av = [k for k in av if k != rand] # remove rand from the check
			
		#print(S)
	
	return 00
	
def valid(x,y,z,r,opp):
	#print(r)
	#print('z: ', z, 'x: ', x, 'y: ', y)
	if r in x: # already game sceduled in team season schedule
		#print('y')
		return False
	elif r in y: # already game scheduled in week against this team
		#print('x')
		return False

	elif opp in z: # opposing team already has a game scheduled in their season
		#print('z')
		return False
	else:
		return True


	return False

def fun(v):
	return (1 + (math.sqrt(v) * math.log(v/2)))

def cost(S):		
	totalCos = 0

	
	for team in range(len(S)):
		i = team
		
		for week in range(len(S[team])):
			
			j = week
			#print(j)

			startL = 0
			destL = 2
			#print(week)
			if j is 0:
				startL = i
			else:
				if S[i][j-1] > 0:
					startL = i
				else:
					startL = abs(S[team][week-1]) -1
			
			if j is len(S[team]):
				destL = i
			else:
			#	print('x')
				if S[team][week] > 0:
					destL = i
				else:
			#		print(S[team][week])
					destL = abs(S[team][week]) -1
			#print(startL, '   ', destL)
			#print('cost', costMat[startL][destL])
			totalCos += float(abs(int(costMat[startL][destL])))
			if j is len(S[team]) - 1:
				totalCos+= float(abs(int(costMat[destL][team])))
		#print((abs(S[team][-1]) - 1), '   ', team)
		#b = float(abs(costMat[(abs(S[team][-1])) - 1][team]))
		#print('cost', b)
		#totalCos += b
	return (totalCos)

def violations(S):
	viol = 0
	counter = 0
	for team in range(len(S)):
		for week in range(len(S[team])):
			if S[team][week] == 00:
				viol+= costNorm*2
			if week > 2:	
				if S[team][week-3] < 0 and S[team][week-2] < 0 and S[team][week-1] < 0 and  S[team][week] < 0:
				
					viol += costNorm*1
				
				if S[team][week-3] > 0 and S[team][week-2] > 0 and S[team][week-1] > 0 and  S[team][week] > 0:
					viol += costNorm*1
			if week > 0:	
				if abs(S[team][week]) == abs(S[team][week-1]):
					viol += costNorm*2
	return viol
	
def fitness(S):

	viol = violations(S)
	cos = cost(S)
	violation.append(viol)
	costs.append(cos)
	return - (cos + viol)
	
	
	
def schedule_full(S):
	for team in S:
		for week in team:
			if week is None:
				#print("not full")
				return False
				
	return True
	
def normalise_mat(M):
	N = [[None for x in range(6)] for x in range(6)]
	min = M[0][0]
	max = 0
	
	for x in M:
		for y in x:
			if y < min and y != 0:
				min = y
			if y > max:
				max = y
				
	for x in range(len(M)):
		for y in range(len(M[x])):
			#print(x,y)
			if M[x][y] == 0:
				N[x][y] = 0
			else:
				N[x][y] = (M[x][y] - min) / (min - max)
	
	return N
	

#costMat = [[0, 3010, 1120, 2010, 300, 1000], [3010, 0, 1230, 2010, 1120, 3010], [1120, 1230, 0, 1120, 100, 3030], [2010, 2010, 1120, 0, 220, 1110], [300, 1120, 100, 220, 0, 1120], [1000, 3010, 3030, 1110, 1120, 0]]
costMat = [[0, 745, 665, 929],[745, 0, 80, 337],[665, 80, 0, 380],[929, 337, 380, 0]]
costMat =  [[0,  745,  665,  929, 605,  521,  370,  587,  467,  670,  700, 1210, 2130, 1890, 1930, 1592],
			[745,   0,   80,  337, 1090,  315,  567,  712,  871,  741, 1420, 1630, 2560, 2430, 2440, 2144],
			[665,  80,    0,  380, 1020,  257,  501,  664,  808,  697, 1340, 1570, 2520, 2370, 2390, 2082],
			[929, 337,  380,    0, 1380,  408,  622,  646,  878,  732, 1520, 1530, 2430, 2360, 2360, 2194],
			[605, 1090, 1020, 1380,   0, 1010,  957, 1190, 1060, 1270,  966, 1720, 2590, 2270, 2330, 1982],
			[521,  315,  257,  408, 1010,   0, 253,  410,  557,  451, 1140, 1320, 2260, 2110, 2130, 1829],
			[370,  567,  501,  622,  957,  253,  0,  250,  311,  325,  897, 1090, 2040, 1870, 1890, 1580],
			[587,  712,  664,  646, 1190,  410,  250,   0,  260,   86, 939,  916, 1850, 1730, 1740, 1453],
			[467,  871,  808,  878, 1060,  557,  311,  260,   0,  328,  679,  794, 1740, 1560, 1590, 1272],
			[670,  741,  697,  732, 1270,  451,  325,   86, 328,    0, 1005, 905, 1846, 1731, 1784, 1458],
			[700, 1420, 1340, 1520,  966, 1140,  897,  939,  679, 1005,   0,  878, 1640, 1300, 1370, 1016],
			[1210, 1630, 1570, 1530, 1720, 1320, 1090,  916,  794,  905,  878,   0,  947,  832,  830,  586],
			[2130, 2560, 2520, 2430, 2590, 2260, 2040, 1850, 1740, 1846, 1640, 947,  0,  458,  347,  654],
			[1890, 2430, 2370, 2360, 2270, 2110, 1870, 1730, 1560, 1731, 1300, 832, 458,   0,  112,  299],
			[1930, 2440, 2390, 2360, 2330, 2130, 1890, 1740, 1590, 1784, 1370, 830,  347,  112,   0,  358],
			[1592, 2144, 2082, 2194, 1982, 1829, 1580, 1453, 1272, 1458, 1016, 586,  654,  299, 358,    0]]
#print(costMat)

#	print(c)

#costMat
#costMat
csum = 0
for col in costMat:
	for item in col:
		csum += (item*item)

costNorm = np.sqrt(csum)
#print(costNorm)
args = sys.argv
gener = int(args[1])
slv = int(args[2])
teamsize = int(args[3])
random.seed(int(args[4]))

#print(gener, slv, teamsize)
if teamsize == 0:
	num = 4
else:
	num = (teamsize*2) + 4
cfile = 'data' + str(num) + '.txt'
c = open(cfile, 'r')
#cost = []
readcos = np.array(c.read().split())

for item in readcos:
	item = int(item)
readcos = np.reshape(readcos, (num, num))
costMat = readcos
	
#normMat = normalise_mat(costMat)
#a = np.array([[3,2,4,-3,-2,-4],[4,-1,-3,-4,1,3],[-1,4,2,1,-4,-2],[-2,-3,-1,2,3,1]])
#print(a)
#print(fitness(a))
#pdb.set_trace()
#print(normMat)
#costMat = [[0, 10, 20, 10], [10, 0, 30, 10], [20, 30, 0, 20], [10, 10, 20, 0]]



if teamsize == 0:
	teams = 4
else:
	teams = (teamsize*2) + 4

if slv == 0:
	if gener == 0:
		file =  './aHC' + 'start1' + '_' + str(teams) + '_' + str(args[4]) + '.dat'
	elif gener == 1:
		file =  './aHC' + 'start2' + '_' + str(teams) + '_' + str(args[4]) + '.dat'

	slv = "HC"
		
if slv == 1:
	if gener == 0:
		file =  './aEA' + 'start1' + '_' + str(teams) + '_' + str(args[4]) + '.dat'
	elif gener == 1:
		file =  './aEA' + 'start2' + '-' + str(teams) + '_' + str(args[4]) + '.dat'
	slv = "EA"
weeks = (2 * teams) - 2
f=open(file, 'a')
#S = start1()
#print(S)
#print(cost(S))
#print(violations(S))
#print('exit')
		
history = []
hist = []
matrices = []
violation = []
costs = []
if gener == 0:
	gen = start1
if gener == 1:
	gen = start2
budj = (teams*teams) * 100000

violation = []
start_time = time.time()
fit,ind = solve(gen,fitness, solver = slv,str_trace = True, budget = budj)
finish_time = time.time() - start_time
history = solve.data
solution = []
#print(fit)
for x in fit:
	for y in x:
		solution.append(y)
#print(violations)
write = str(gen) + '	' + slv + '	' + str(teams) + '	' + str(args[4])+ '	' + str(budj)+ '	' + str(solution) + '	' + str(ind) + '	' + str(history) + '	' + str(violation) + '	' + str(costs) + '\n'
f.write(write)
	#print(write)

#fig	 = plt.figure()
#ax = plt.axes()
	
	#print(fit, normMat, ind)
#ax.plot(history);
#plt.show()
f.close()
#print(history)
#print("Solver:",fit,"-----", ind)
#print("Time: ", time.time() - start_time)
