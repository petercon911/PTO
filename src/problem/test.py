from PTO import random,random_function,solve,plot_runs, compare_all, make_table, stat_summary, plot_scalability
import math, time, pdb
import copy
random.seed(0)

def start():
	S = [[None for x in range(weeks)] for x in range(teams)]
	
	#S = randomPerm(S)
	#S = randomPerm2(S)
	S = randomPerm3(S)
	
	print("end", S)
	#pdb.set_trace()

	return S
	

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
		print(S)
		print(spaceNone)
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
	
@random_function	
def randomPerm2(S):
	teamLength = [k for k in range(teams)]
	
	for i in range(teams):
		o = random.choice(teamLength)
		weekLength = [k for k in range(weeks)]
		for j in range(weeks):
			#print(weekLength)
			
			p = random.choice(weekLength)
			if S[o][p] == None:
				temp = getGame2(o,p,S)
				print(o, '  ', p, '  ', temp)
				S[o][p] = temp
				if temp > 0:
					S[abs(temp)-1][j] = -(o + 1)
				else:
					S[abs(temp)-1][j] = o + 1
			
			weekLength.remove(p)
		teamLength.remove(o)
	return S

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
		if b[y-1] != None and b[y-2] != None:
			if b[y-1] <0 and b[y-2] <0:
				available = [k for k in available if k > 0] # no repreat home or away
			if b[y-1] >0 and b[y-2] >0:
				available = [k for k in available if k < 0]
			if abs(b[y-1]) == abs(b[y-2]):
				available = [k for k in available if k != b[y-2]] # no consecutive games
#				print('t ', b)
			
				#print(b[y-1])
			available = [k for k in available if abs(k) != (abs(b[y-1]))] #cannot play the team before again

			available = [k for k in available if S[(abs(k)-1)][y] != None]
	
	if len(available) > 3:
		highest = 0
		marker = 0
		for k in available:
			temp = abs(costMat[x][y] - costMat[abs(k-1)][y])
			if temp > highest:
				highest = temp
				marker = k
		available.remove(k)
		
	if len(available) < 1:
		return 0
	else:
		return random.choice(available)
	
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
		if len(av) == 0:
			raise ValueError("HI")
		
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
				
			if valid(a,b,S[abs(rand)-1],rand,opp): 	# check if rand and opp are valid
				return rand
			
		av.remove(rand) # remove rand from the check
			
		#print(S)
	
	return 00
	
def valid(x,y,z,r,opp):
	#print(r)
	#print('z: ', z, 'x: ', x, 'y: ', y)
	if r in x: # already game scheduled in week against this team
		print('x')
		return False
	elif r in y: # already game sceduled in team season schedule
		print('y')
		return False
	elif opp in z: # opposing team already has a game scheduled in their season
		print('z')
		return False
	else:
		return True


	return False

def fun(v):
	return (1 + (math.sqrt(v) * math.log(v/2)))

def cost(S):		
	totalCos = 0

	
	for team in S:
		i = S.index(team)
		
		for week in team:
			if week == 00:
				break
			j = team.index(week)
			#print(week)
			if j is 0:
				startL = i
			else:
				if S[i][j-1] > 0:
					startL = i
				else:
					startL = abs(week) -1
			
			if j is len(team) - 1:
				destL = i
			else:
				if week > 0:
					destL = i
				else:
					destL = abs(week) -1
			#print(startL, '   ', destL)
			totalCos += int(costMat[startL][destL])
			
	return (totalCos)

def violations(S):
	viol = 0
	counter = 0
	for team in range(len(S)):
		for week in range(len(S[team])):
			if S[team][week] == 00:
				counter+= 1
				if counter > 0:
					viol += 1000000000
				if counter > 3:
					viol += 100000000
				if counter > 6:
					viol += 100000000000
				
			if S[team][week-3] < 0 and S[team][week-2] < 0 and S[team][week-1] < 0 and  S[team][week] < 0:
				viol += 1000000
				
			if S[team][week-3] > 0 and S[team][week-2] > 0 and S[team][week-1] > 0 and  S[team][week] > 0:
				viol += 1000000
	return viol
	
def fitness(S):

	viol = violations(S)
	
	if viol == 0:
		return - int(cost(S))
		
	else:
		return - int(math.sqrt(cost(S)**2 + (fun(viol)**2)))
	
	
	
def schedule_full(S):
	for team in S:
		for week in team:
			if week is None:
				print("not full")
				return False
				
	return True
	
teams = 6
weeks = (2 * teams) - 2
costMat = [[0, 3010, 1120, 2010, 300, 1000], [3010, 0, 1230, 2010, 1120, 3010], [1120, 1230, 0, 1120, 100, 3030], [2010, 2010, 1120, 0, 220, 1110], [300, 1120, 100, 220, 0, 1120], [1000, 3010, 3030, 1110, 1120, 0]]
#costMat = [[0, 10, 20, 10], [10, 0, 30, 10], [20, 30, 0, 20], [10, 10, 20, 0]]

#S = start()
#print(S)
#print(cost(S))
#print(violations(S))
start_time = time.time()

fit,ind = solve(start,fitness, solver = "HC",str_trace = True, budget = 1000)
history = solve.data
print(history)
print("Solver:",fit,"-----", ind)
print("Time: ", time.time() - start_time)
