#from PTO import random, random_function, solve
import random
def start():
	S = [[None for x in range(weeks)] for x in range(teams)]
	
	S = randomPerm(S)

	
	return S
	
def randomPerm(S):
	for i in range(teams):
		for j in range(weeks):
			S[i][j] = getGame(i,j,S)
			
	return S
	
def getGame(x,y,S):
	easyR = [[None for x in range(weeks)] for x in range(teams)]
	for i in range(teams):
		easyR[i][y] = S[i][y] # building a T matrix of relevant possible violations
	
	for i in range(weeks):
		easyR[x][i] = S[x][i]
	
	available = [x for x in range(-teams, teams + 1)]
	available = [x for x in available if x != 0]
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
	print('t ', checkTeam, '  ', y)
	if checkTeam != []:
		print(checkTeam[y-1])
		available = [k for k in available if abs(k) != abs(checkTeam[y-1])]
	for i in range(len(checkWeek)):
		try:
			available.remove(i + 1)
		except:
			print('y')
		try:
			available.remove(-(i + 1))
		except:
			print('z')
			
	print('w ', checkWeek)
	print('t ', checkTeam)
	print('a ', available)
	print(y)
	
	if len(checkTeam) > 2:
		if checkTeam[y-1] <0 and checkTeam[y-2] <0:
			available = [k for k in available if k > 0] # no repreat home or away
		if checkTeam[y-1] >0 and checkTeam[y-2] >0:
			available = [k for k in available if k < 0]
		if abs(checkTeam[y-1]) == abs(checkTeam[y-2]):
			available = [k for k in available if k != checkTeam[x-2]]
#			print('t ', checkTeam)
			
		
	if (x + 1) in checkWeek:
		rand = -(checkWeek.index(x+1) + 1)
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

def Cost(S):
	totalCos = 0
	costMat = [[0, 10, 20, 30], [10, 0, 10, 20], [20, 10, 0, 20], [30, 20, 20, 0]]
	
	for team in S:
		i = S.index(team)
		
		for week in team:
			if week == 100:
				break
			j = team.index(week)
			print(week)
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
			print(startL, '   ', destL)
			totalCos += int(costMat[startL][destL])
			
	return (totalCos)

def violations(S):
	viol = 0
	
	for team in S:
		for week in team:
			if week == 100:
				viol += 100
	
	return viol
	
teams = 4
weeks = (2 * teams) - 2

S = start()
print(S)
print(Cost(S))
print(violations(S))