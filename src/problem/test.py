from PTO import random,random_function,solve,plot_runs, compare_all, make_table, stat_summary, plot_scalability
import math
import copy

def start():
	S = [[None for x in range(weeks)] for x in range(teams)]
	
	#S = randomPerm(S)
	S = randomPerm2(S)
	
	return S
	

def randomPerm(S):
	for i in range(teams):
		for j in range(weeks):
			S[i][j] = getGame(i,j,S)
			
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
			
		
	if (x + 1) in checkWeek:
		rand = -(checkWeek.index(x+1) + 1) # fill in the opposite number for each selection
	elif -(x + 1) in checkWeek:
		rand = checkWeek.index(-(x+1)) + 1
	else:
		try:
			rand = random.choice(available)
		except:
			rand = 100
	
	

	
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
			
		
	return rand
	
def randomPerm2(S):
	for i in range(teams):
		for j in range(weeks):
			if S[i][j] == None:
				temp = getGame2(i, j, S)
				print(temp)
				S[i][j] = temp
				if temp > 0:
					S[abs(temp)-1][j] = -(i + 1)
				else:
					S[abs(temp)-1][j] = i + 1

	return S
	
def getGame2(x,y,S):
	# build available without 0 or the current team
	available = [i for i in range(-teams, teams + 1) if i != 0 and abs(i) != (x + 1)]
	rand = 100; 
	a = []; b = [];
	for i in range(teams):
		a.append(S[i][y])
	for i in range(weeks):
		b.append(S[x][i])
	
	#print(available)
	#print(a)
	#print(b)

	for r in range(len(available)): 
		rand = random.choice(available)
		print(available)
		z = [];
		if S[abs(rand) - 1][y] == None: # opposite isn't full
			if rand > 0:
				opp = -(x+1)	# create opposite value
			else:
				opp = x + 1
			for i in range(weeks):
				z.append(S[abs(rand)-1][i]) # create opposite row
			if valid(a,b,z,rand,opp): 	# check if rand and opp are valid
				return rand
			else:
				available.remove(rand) # remove rand from the check
			
		print(S)
	
	return 00
	
def valid(x,y,z,r,opp):
	print(r)
	print(z)
	if r in x: # already game scheduled in week against this team
		print('z')
		return False
	elif r in y: # already game sceduled in team season schedule
		print('x')
		return False
	elif opp in z: # opposing team already has a game scheduled in their season
		print('y')
		return False
	else:
		return True


	return False

def cost(S):		
	totalCos = 0
	costMat = [[0, 10, 20, 10, 30, 10], [10, 0, 30, 10, 20, 10], [20, 30, 0, 20, 10, 30], [10, 10, 20, 0, 20, 10], [30, 20, 10, 20, 0, 10], [10, 10, 30, 10, 10, 0]]
	#costMat = [[0, 10, 20, 10], [10, 0, 30, 10], [20, 30, 0, 20], [10, 10, 20, 0]]
	
	for team in S:
		i = S.index(team)
		
		for week in team:
			if week == 100:
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
	
	for team in S:
		for week in team:
			if week == 100:
				viol += 100
	
	return viol
	
def fitness(S):
	fitness = - int(violations(S) + cost(S))
	return fitness
	
teams = 6
weeks = (2 * teams) - 2

S = start()
print(S)
#print(cost(S))
#print(violations(S))

#fit,ind = solve(start,fitness, solver = "HC",str_trace = True, budget = 100)
#history = solve.data
#print(history)
#print("Solver:",fit,"-----", ind)
