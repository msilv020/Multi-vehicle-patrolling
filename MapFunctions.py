# global startPoint, visDistance, energyBudget, crit_points
import MapProperties


def var_ground():	#Modifies variables for ground use
	MapProperties.startPoint = (225,90)
	MapProperties.visDistance = 3			#visibility range = visDistance * 5
	MapProperties.energyBudget = 112 		#the diagonal of the graph = 559 rounded to 560
	MapProperties.crit_points = [(350,115),(380,15),(50,50),(190,200),(25,140)]	#points that should be checked if possible

def var_air():		#modifies variables for air use
	MapProperties.startPoint = (225,90)
	MapProperties.visDistance = 6			#twice the visibility of ground
	MapProperties.energyBudget = 112		#half the budget of ground
	MapProperties.crit_points = [(350,115),(380,15),(50,50),(190,200),(25,140),(300,220),(450,75)]	#points that should be checked if possible

def var_sea():		#Modifies variables for sea use
	MapProperties.startPoint = (400,200)	
	MapProperties.visDistance = 3			#visibility range = visDistance * 5
	MapProperties.energyBudget = 112 		#the diagonal of the graph = 559 rounded to 560
	MapProperties.crit_points = [(300,220),(450,75)]


def create_map(graph):#layout nodes and edges for entire 500 X 250 area
	for i in range (100+1):
		for j in range (50+1):
			graph.add_node((i*5,j*5))
			
	for i in range (50): #add edges to left and right most columns
		graph.add_edge((0,i*5),(0,i*5+5), weight = 1.0)
		
	for i in range (50):	
		graph.add_edge((500,i*5),(500,i*5+5), weight = 1.0)
		
		if (i>0):
			graph.add_edge((495,i*5),(500,i*5-5), weight = 1.414)#edge to North West
		if (i < 1): 
			graph.add_edge((495,i*5),(500,i*5+5), weight = 1.414)#edge to North East

	for j in range (1,100): #add edges to top and bottom rows
		graph.add_edge((j*5,0),(j*5+5,0), weight = 1.0)
		graph.add_edge((j*5,0),(j*5-5,0), weight = 1.0)#edge to East
		if (j>0): graph.add_edge((j*5,0),(j*5-5,5), weight = 1.414)#edge to North West

	for j in range (100):	
		graph.add_edge((j*5,250),(j*5+5,250), weight = 1.0)
		if (j == 1): 
			graph.add_edge((0,245),(5,250), weight = 1.414)#edge to South West
			graph.add_edge((495,250),(500,245), weight = 1.414)#edge to South West

	for i in range(1,100):#fill node edges
		for j in range(1,50):
			graph.add_edge((i*5,j*5),(i*5,j*5+5), weight = 1.0)#edge to North
			graph.add_edge((i*5,j*5),(i*5+5,j*5+5), weight = 1.414)#edge to North East
			graph.add_edge((i*5,j*5),(i*5+5,j*5), weight = 1.0)#edge to East
			graph.add_edge((i*5,j*5),(i*5-5,j*5-5), weight = 1.414)#edge to South East
			
			graph.add_edge((i*5,j*5),(i*5,j*5-5), weight = 1.0)#edge to South
			graph.add_edge((i*5,j*5),(i*5-5,j*5-5), weight = 1.414)#edge to South West
			graph.add_edge((i*5,j*5),(i*5-5,j*5), weight = 1.0)#edge to West
			graph.add_edge((i*5,j*5),(i*5-5,j*5+5), weight = 1.414)#edge to North West


def ground_map(graph):			
	for i in range(19):#Loops to remove nodes creating an obstacle**************************
		for j in range(8):
			graph.remove_node((275+i*5,10+j*5))
				
	for i in range(28):
		for j in range(18):
			graph.remove_node((40+i*5,250-105+j*5))
	 
	for i in range(23):
		for j in range(5):
			graph.remove_node((145+i*5,250-145+j*5))

	for i in range(23):
		for j in range(11):
			graph.remove_node((115+i*5,15+j*5))
	 
	for i in range(14):
		for j in range(4):
			graph.remove_node((280+i*5,60+j*5))
			
	for i in range(8):
		for j in range(2):
			graph.remove_node((230+i*5,70+j*5))

	for i in range(22):		#water and forest removal**************************************
		for j in range(51):
			graph.remove_node((395+i*5,j*5))		
			
	for i in range(26):
		for j in range(21):
			graph.remove_node((265+i*5,150+j*5))
				
	for i in range(13):
		for j in range(24):
			try:
				graph.remove_node((200+i*5,150+j*5))
			except:
				continue
	
	# startPoint = (225,90)
	# visDistance = 3			#visibility range = visDistance * 5
	# energyBudget = 112 		#the diagonal of the graph = 559 rounded to 560
	# crit_points = [(350,115),(380,15),(50,50),(190,200),(25,140)]


def air_map(graph):#layout nodes and edges for entire 500 X 250 area
	for i in range (100+1):
		for j in range (50+1):
			graph.add_node((i*5,j*5))
			
	for i in range (50): #add edges to left and right most columns
		
		graph.add_edge((0,i*5),(0,i*5+5), weight = 1.0)
		
	for i in range (50):	
		graph.add_edge((500,i*5),(500,i*5+5), weight = 1.0)
		
		if (i>0):
			graph.add_edge((495,i*5),(500,i*5-5), weight = 1.414)#edge to North West
		if (i < 1): 
			graph.add_edge((495,i*5),(500,i*5+5), weight = 1.414)#edge to North East

	for j in range (1,100): #add edges to top and bottom rows
		graph.add_edge((j*5,0),(j*5+5,0), weight = 1.0)
		graph.add_edge((j*5,0),(j*5-5,0), weight = 1.0)#edge to East
		if (j>0): graph.add_edge((j*5,0),(j*5-5,5), weight = 1.414)#edge to North West

	for j in range (100):	
		graph.add_edge((j*5,250),(j*5+5,250), weight = 1.0)
		if (j == 1): 
			graph.add_edge((0,245),(5,250), weight = 1.414)#edge to South West
			graph.add_edge((495,250),(500,245), weight = 1.414)#edge to South West

	for i in range(1,100):#fill node edges
		for j in range(1,50):
			graph.add_edge((i*5,j*5),(i*5,j*5+5), weight = 1.0)#edge to North
			graph.add_edge((i*5,j*5),(i*5+5,j*5+5), weight = 1.414)#edge to North East
			graph.add_edge((i*5,j*5),(i*5+5,j*5), weight = 1.0)#edge to East
			graph.add_edge((i*5,j*5),(i*5-5,j*5-5), weight = 1.414)#edge to South East
			
			graph.add_edge((i*5,j*5),(i*5,j*5-5), weight = 1.0)#edge to South
			graph.add_edge((i*5,j*5),(i*5-5,j*5-5), weight = 1.414)#edge to South West
			graph.add_edge((i*5,j*5),(i*5-5,j*5), weight = 1.0)#edge to West
			graph.add_edge((i*5,j*5),(i*5-5,j*5+5), weight = 1.414)#edge to North West

	# # global startPoint, visDistance, energyBudget, crit_points
	# startPoint = (225,90)
	# visDistance = 6			#twice the visibility of ground
	# energyBudget = 56 		#half the budget of ground
	# crit_points = [(350,115),(380,15),(50,50),(190,200),(25,140),(400,200),(450,100)]

			
def sea_map(graph):#remove ground area nodes
	for i in range (54):
		for j in range(51):
			try:
				graph.remove_node((i*5,j*5))
			except:
				continue
			
	for i in range (26):
		for j in range(30):
			try:
				graph.remove_node((270+i*5,j*5))	
			except:
				continue	

	for i in range (5):
		for j in range(51):
			try:
				graph.remove_node((480+i*5,j*5))	
			except:
				continue
				
	# startPoint = (450,220)
	# visDistance = 3			#visibility range = visDistance * 5
	# energyBudget = 112 		#the diagonal of the graph = 559 rounded to 560
	# crit_points = [(400,200),(450,100)]			