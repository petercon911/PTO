from PTO import random,random_function,solve,plot_runs, compare_all, make_table, stat_summary, plot_scalability
import math
import copy


## 1) define your random solution generator

 # Builds a random starting schedule to build and improve on
@random_function 
def randsol():
    # Create an empty schedule
    S = [[None for i in range(weeks)] for j in range(number_teams)]
    #return S
    # Call the recursive build function
#    result_S = random_move
    result_S = r_randsol(S, 0, 0)
#    S_prime = copy.deepcopy(result_S)
#    S_prime = random_move(result_S)
#    print(result_S)
#    print(nbv(result_S),fitness(result_S))

#    print(len(result_S))
#    print(result_S)
    return result_S

#def new_f(S):
#    for team in range(len(S)):
#        for game in range(1, len(S[team])):          
#
#                
#                
#
#        for game in range(1,len(S[team])):
#            if S[team][game-3][1] == 1 and S[team][game-2][1] == 1 and S[team][game-1][1] == 1 and S[team][game][1] == 1:
##      
#                violations += 1
#
#            elif  S[team][game-3][1] == 0 and S[team][game-2][1] == 0 and S[team][game-1][1] == 0 and S[team][game][1] == 0 :
##                 
#                violations += 1

  
def schedule_full(S):
        for week in S:
            for game in week:
                if game is None:
                    return False
        return True

 # Given the schedule and an empty slot, determine the possible games that can be scheduled here
@random_function
def get_game(S, i, j):
    # Create a list of available teams
    home = lambda x: (x, 1)
    away = lambda x: (x, 0)
    available = [f(x) for x in range(1, number_teams+1) for f in (home, away)]
#    print(available)
#    

    # Remove self from list
    available = [k for k in available if k[0] is not i+1]
#    print(available)

    # Remove games that this team already has on its schedule
    available = [l for l in available if l not in S[i]]
#    available = [l for l in available if ]
#    print(available)
    

    # Remove opponents that are in concurrent games
    col = [o[0] for o in [row[j] for row in S] if o is not None]
#    print(col)
    available = [m for m in available if m[0] not in col]
#    print('Available:',available)

    return available

# Given the schedule and a specfic match, schedule the opponent for that match
@random_function
def set_opponent(S, i, j):
    match = S[i][j]
    if match[1] is 1 :
        S[match[0]-1][j] = (i+1, 0)
    else:
        S[match[0]-1][j] = (i+1, 1)
#    print(S)

    return S

# Recursive part of build schedule
@random_function
def r_randsol(S, team, week):
    # If the schedule is full then return becuase it is complete
    
    if schedule_full(S):
#        print("Schedule full:", schedule_full(S))
        return S
    

    # Calculate the next location
    next_week = week + 1
    next_team = team
    if next_week == weeks:
        next_week = 0
        next_team += 1

    # If there is already a game scheduled then move forward
    if S[team][week] is not None:
        return r_randsol(S, next_team, next_week)

    # Find all of the possible games that can be scheduled, return if it isn't schedulable
    possibilities = get_game(S, team, week)
#    print(possibilities)
    random.shuffle(possibilities)
    if possibilities is None:
        return None

    # Try all the possible games until one works
    for p in possibilities:
#        print('P',p)
        try_S = [[c for c in r] for r in S]
#        print('Try S',try_S)
        # Set the game as well as the opponent
        try_S[team][week] = p
        set_opponent(try_S, team, week)
        # Move forward with this attempt
        result_S = r_randsol(try_S, next_team, next_week)
        if result_S is not None:
            return result_S

    # Catch all
    return None
## 2) define your fitness function 
    # Calculate the cost of the input schedule
def cost(S):
    total_cost = 0
    cost_m = cost_matrix
    #print("Cost Matrix:",cost_m)
    # Loop through the schedule calculating the cost along the way
    for team in S:
        i = S.index(team)
#        print(i)
        team.append((None, 1))
#        print(team.append((None, 1)))
        for game in team:
            j = team.index(game)
            start_loc = None
            dest_loc = None
            # Handle the first game case, get start location
            if j is 0:
                start_loc = i
            else:
                if team[j-1][1] is 1:
                    start_loc = i
                else:
                    start_loc = team[j-1][0] - 1


            # Handle the last game case, get the travel location
            if j is len(team) - 1:
                dest_loc = i
            else:
                if team[j][1] is 1:
                    dest_loc = i
                else:
                    dest_loc = team[j][0] - 1
            # Cost
#            print(start_loc,dest_loc)
            total_cost += int(cost_m[start_loc][dest_loc])
#            print (total_cost)
        # Pop off the placeholder location
#        print(team)
        team.pop()
#    print(total_cost)
    return (total_cost)



# Determine the number of violations in a given schedule
def nbv(S):
    violations = 0
#     Loop through the schedule looking for non-repeat violations

    for team in range(len(S)):
        for game in range(1, len(S[team])):          
            if S[team][game][0] == S[team][game - 1][0]:
                violations +=1

        for game in range(1,len(S[team])):
            if S[team][game-3][1] == 1 and S[team][game-2][1] == 1 and S[team][game-1][1] == 1 and S[team][game][1] == 1:
#      
                violations += 1

            elif  S[team][game-3][1] == 0 and S[team][game-2][1] == 0 and S[team][game-1][1] == 0 and S[team][game][1] == 0 :
#                 
                violations += 1
                


#    print(violations)
                    
#            
#
#        for game in range(1, len(S[team])):
#            if S[team][game-1][0] is S[team][game][0]:
#                violations += 1

    return violations
#                print(violations)

#    # Loop through the schedule looking for atmost violations
#    for team in range(len(S)):
#        for game in range(3,len(S[team])):
#                if S[team][game-3][1] == "home" and S[team][game-2][1] == "home" and S[team][game-1][1] == "home" and S[team][game][1] == "home":
##      
#                    violations += 1
#
#                if S[team][game-3][1] == 0 and S[team][game-2][1] == 0 and S[team][game-1][1] == 0 and S[team][game][1] == 0 :
##                 
#                    violations += 1
#                    
#    for team in range(len(S)):
#       for game in range(1, len(S[team])):
#           if S[team][game][0] != -S[team][game - 1][0]:
#               violations +=1
####     
##    print(violations)
#    return violations  


# define fun (f function)
def fun(v):
#    print("test:",1 + math.sqrt(v) * math.log(v / 2))
    return (1 + (math.sqrt(v) * math.log(v/2)))

# # Calculate the TTSA cost
def fitness(S):
#    weight = 4000
#    teta = 1.04
    
    if nbv(S) == 0:
#        weight = weight/teta
#        print(-int(cost(S)))
        return int(-cost(S))
    else:
#        print(-int((math.sqrt(cost(S)**2 + (fun(nbv(S))**2)))))
#        weight = weight * teta
        return -int(math.sqrt(cost(S)**2 + (fun(nbv(S))**2)))

## 3) optimize it!
## 4) ... and analise it
# Builds the cost matrix for the coresponding number of teams

def get_cost_matrix(number_teams):
    file_name = "super" + str(number_teams) + ".txt"
    l = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                l.append(line.split())
#                print("l",l)
    print(l)
    return l



##    # Given a game, swap the home/awayness of that game
def home_away(game):
    if game[1] == 1:
        return (game[0], 0)
    else:
        return (game[0], 1)
        
 #   the choice is just made inside of the function instead of being passed in.
def swap_homes(S):
    # Choose a team to swap on
    team  = len(S) - 1
    swap_loc = S[team].index(random.choice(S[team]))
    swap_loc_mirror = S[team].index(home_away(S[team][swap_loc]))

    # Swap the first game and its opponent
    S[team][swap_loc] = home_away(S[team][swap_loc])
    S = set_opponent(S, team, swap_loc)

    # Swap the matching game and its opponent
    S[team][swap_loc_mirror] = home_away(S[team][swap_loc_mirror])
    S = set_opponent(S, team, swap_loc_mirror)
    #print("Swap_homes:",S)
    return S

def swap_rounds(S):
        # Choose two different rounds to swap
        choices = random.sample(list(range(len(S[0]))), 2)

        # Iterate through the teams swapping each rounds
        for team in range(len(S)):
            game_one = S[team][choices[0]]
            game_two = S[team][choices[1]]
            S[team][choices[0]] = game_two
            S[team][choices[1]] = game_one

        return S


def swap_teams(S):
        # Choose two different teams to swap
        choices = random.sample(list(range(len(S))), 2)

        # Swap the teams completely
        team_one = S[choices[0]]
        team_two = S[choices[1]]
        S[choices[0]] = team_two
        S[choices[1]] = team_one

        # Resolve the same team conflicts
        for game in range(len(S[choices[0]])):
            # If the team is playing itself fix it and resolve opponent
            if S[choices[0]][game][0] - 1 is choices[0]:
                S[choices[0]][game] = home_away(S[choices[1]][game])
                S = set_opponent(S, choices[0], game)

        # Resolve the opponents
        for team in choices:
            for game in range(len(S[team])):
                S = set_opponent(S, team, game)

        return S    

 # Swap games by same round different teams and resolve opponents
def swap_game_team(S, r, T1, T2):
    game_one = S[T1][r]
    game_two = S[T2][r]
    S[T1][r] = game_two
    S[T2][r] = game_one
    S = set_opponent(S, T1, r)
    S = set_opponent(S, T2, r)
    return S

# Swap games by same team different rounds
def swap_game_round(S, t, rl, rk):
    game_one = S[t][rl]
    game_two = S[t][rk]
    S[t][rl] = game_two
    S[t][rk] = game_one
    return S

    
def partial_swap_rounds(S):
        # Choose a random team and two random rounds to swap
        s_team = random.sample(list(range(len(S))), 1)[0]
        s_rounds = random.sample(list(range(len(S[0]))), 2)

        # Create a starting list
        p_swap = [s_team]

        # Chain ejection until everything is in the list
        while 1:
            # loop through the list adding new teams if necessary
            for item in p_swap:
                if S[item][s_rounds[0]][0]-1 not in p_swap:
                    p_swap.append(S[item][s_rounds[0]][0]-1)

                if S[item][s_rounds[1]][0]-1 not in p_swap:
                    p_swap.append(S[item][s_rounds[1]][0]-1)

            # Check to see if the list is fully inclusive
            if (S[p_swap[-1]][s_rounds[0]][0]-1 in p_swap) and (S[p_swap[-1]][s_rounds[1]][0]-1 in p_swap) and (S[p_swap[-2]][s_rounds[0]][0]-1 in p_swap) and (S[p_swap[-2]][s_rounds[1]][0]-1 in p_swap):
                break

        # Loop through the list for one of the rounds and swap all the games in the list
        for item in p_swap:
            S = swap_game_round(S, item, s_rounds[0], s_rounds[1])

        return S
    
@random_function
def get_concurrent(S, T1, T2, game):
        for i, j in enumerate(S[T1]):
            if j == game:
                return S[T2][i]

def partial_swap_teams(S):
        # Choose a random round and two random teams to swap
        s_round = random.sample(list(range(len(S[0]))), 1)[0]
        s_teams = random.sample(list(range(len(S))), 2)

        # Handle case where the games cannot be swapped because it is invalid (cant play yourself)
        if not (set(s_teams) - set([S[s_teams[0]][s_round][0]-1, S[s_teams[1]][s_round][0]-1])):
            return S

        # Create a starting list
        p_swap = [S[s_teams[0]][s_round], S[s_teams[1]][s_round]]

        # Chain ejection until everything is in the list
        while 1:
            # Loop through the list adding new teams if necessary
            for item in p_swap:
                if get_concurrent(S, s_teams[0], s_teams[1], item) not in p_swap:
                    p_swap.append(get_concurrent(S, s_teams[0], s_teams[1], item))

                if get_concurrent(S, s_teams[1], s_teams[0], item) not in p_swap:
                    p_swap.append(get_concurrent(S, s_teams[1], s_teams[0], item))

            if( (get_concurrent(S, s_teams[0], s_teams[1], p_swap[-1]) in p_swap) and (get_concurrent(S, s_teams[1], s_teams[0], p_swap[-1]) in p_swap) and
                (get_concurrent(S, s_teams[0], s_teams[1], p_swap[-2]) in p_swap) and (get_concurrent(S, s_teams[1], s_teams[0], p_swap[-2]) in p_swap) ):
                break

        # Get the indices of the games found
        p_indices = []
        for item in p_swap:
            p_indices.append(S[s_teams[0]].index(item))

        # Loop through the list for one of the teams and swap all of the games and resolve opponents
        for idx in p_indices:
            S = swap_game_team(S, idx, s_teams[0], s_teams[1])

        return S
@random_function
def random_move(S):
        # Select a random function to call on the schedule
        choice = random.randint(0,4)

        # Select and perform the operation
        if choice is 0:
            return swap_homes(S)
        elif choice is 1:
            return swap_rounds(S)
        elif choice is 2:
            return swap_teams(S)
        elif choice is 3:
            return partial_swap_rounds(S)
        else:
            return partial_swap_teams(S)
    
number_teams = 6
weeks = (2 * number_teams) - 2
#best_feasible_S = []
#best_infeasible_S = []
#result=randsol()
#print("Final Result:",result)
# Make a deepcopy of the schedule
#S_prime = copy.deepcopy(result_S)
#S_prime = random_move(S_prime)
# Read in the cost matrix
cost_matrix = []
cost_matrix = get_cost_matrix(number_teams)

#f = fitness(result)
#print("Fitness:",f)
#print(fitness(randsol()))


#randsol1 = lambda: randsol() # specialise the generator for that instance
#fitness1 = lambda S: fitness(S) # specialise the fitness for that instance

#fit,ind = solve(randsol,fitness, solver = "HC",str_trace = True, budget = 10000)

#print("Solver:",fit,"-----", ind)
#print(nbv(fit))

S = randsol()

print(schedule_full(S))

for week in S:
	print('x')
	for game in week:
		print(game)


