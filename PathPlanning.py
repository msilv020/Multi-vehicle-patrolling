import networkx as nx	
import random
import math

def plan_route(startPoint, G, C, H, crit_points, visDistance, branchStrictness, energyBudget):
	#points to create loop
	a = startPoint
	b = None
	c = None

	#Storage lists
	route = []
	candidates_b = []
	crit_candidates_b = []
	candidates_c = []
	crit_candidates_c = []
	random_c = []
	crit_point_visibility = []
	unseen_candidates_b = []
	unseen_candidates_c = []

	#check if starting point is valid
	if not G.has_node(a):
		print ("Invalid starting point")
		quit()
		
	#check if critical points are valid
	for i in range (len(crit_points)-1):
		if not G.has_node(crit_points[i]):
			print ("Invalid critical point", crit_points[i])
			
	#get points that critical points are visible from
	if len(crit_points) > 0:
		C = nx.ego_graph(G, crit_points[0], radius = visDistance, distance = 'weight')
		for i in range (1,len(crit_points)):
			C = nx.compose(C, nx.ego_graph(G, crit_points[i], radius = 3, distance = 'weight'))
		
	crit_point_visibility = nx.nodes(C)


	shortest_paths_a = nx.single_source_dijkstra_path_length(G, a, cutoff=energyBudget/3, weight='weight')#create dictionary of shortest paths to all nodes 1/3 of energy budget from point a


	for i in range(math.ceil(len(shortest_paths_a)* branchStrictness)):	#takes top 30% of longest paths
		
		key = max(shortest_paths_a, key = lambda k: shortest_paths_a[k])
		candidates_b.append(key)
		del shortest_paths_a[key]
		
	for i in range(len(candidates_b)-1):#put candidates near critical points to new list
		if candidates_b[i] in crit_point_visibility:
			crit_candidates_b.append(candidates_b[i])

	
	#Check for unseen nodes
	# if there are crit candidates add unseen ones to new list otherwise add unseen non crit candidates to new list
	if len(crit_candidates_b) > 0:
		for i in range(len(crit_candidates_b)-1):
			if H.has_node(crit_candidates_b[i]):
				continue
			else:
				unseen_candidates_b.append(crit_candidates_b[i])
				
	if	len(unseen_candidates_b) > 0:
		for i in range(len(crit_candidates_b)-1):
			if H.has_node(candidates_b[i]):
				continue
			else:
				unseen_candidates_b.append(candidates_b[i])		
					
	#pick random b rom appropriate list			
	if (len(unseen_candidates_b) > 0):		#if there are unseen candidates pick random b from unseen candidates	
		b = unseen_candidates_b[random.randint(0, len(unseen_candidates_b)-1)]	
		
	elif(len(crit_candidates_b) > 0):	#if there are crit candidates pick random b from seen crit candidates
		b = crit_candidates_b[random.randint(0, len(crit_candidates_b)-1)]
		
	else:									#pick random b from seen candidates
		b = candidates_b[random.randint(0, len(candidates_b)-1)]

	#dictionary containing shortest paths to all nodes that are (energyBudget/3) from point b
	shortest_paths_b = nx.single_source_dijkstra_path_length(G, b, cutoff=(energyBudget/3), weight='weight')

	#find candidates for c
	for i in range(math.ceil( len(shortest_paths_b)* branchStrictness)):	#takes top 30% of longest paths
		key = max(shortest_paths_b, key = lambda k: shortest_paths_b[k])
		candidates_c.append(key)
		del shortest_paths_b[key]

	for i in range( len(candidates_b)):#Intersect c candidates with b candidates
		for j in range (len(candidates_c)):
			if candidates_b[i] == candidates_c[j]:
				
				random_c.append(candidates_c[j]) #alternate list for picking random c
		

	#Check for unseen nodes
	# if there are crit candidates add unseen ones to new list otherwise add unseen non crit candidates to new list
	if len(random_c) > 0:
		for i in range (len(random_c)-1):
			if random_c[i] in crit_point_visibility:
				unseen_candidates_c.append(random_c[i])
	
	if len(unseen_candidates_c) == 0:
		for i in range(len(random_c)-1):
			if H.has_node(random_c[i]):
				continue
			else:
				unseen_candidates_c.append(random_c[i])
		
				
				
	#pick random c rom appropriate list			
	if (len(unseen_candidates_c) > 0):	#if there are unseen candidates pick random c from unseen candidates	
		c = unseen_candidates_c[random.randint(0, len(unseen_candidates_c)-1)]	
		
	elif(len(random_c) > 0):			#if there are seen candidates pick random c from list
		c = random_c[random.randint(0, len(random_c)-1)]
		
	else:								#pick random c from seen candidates
		print ("Cannot find c candidate in energy budget range return to start point through same route")
		

	
	ab_path = nx.dijkstra_path(G, a, b, weight='weight')	#get shortest path from a to b

	if not c:	#If point c cannot be found return to start through first path taken
		route = ab_path 
	
	else:	#If point c is found connect all points to create route
		bc_path = nx.dijkstra_path(G, b, c, weight='weight')	#get shortest path from b to c
		ca_path = nx.dijkstra_path(G, c, a, weight='weight')	#get shortest path from c to a
		route = ab_path + bc_path + ca_path

		
	return route