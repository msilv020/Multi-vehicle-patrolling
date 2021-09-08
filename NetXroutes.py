import networkx as nx
import matplotlib.pyplot as plt
import pylab as pl
import math
import random
from matplotlib import collections as mc
from PIL import Image
import sys
import getopt
import MapFunctions as map
import MapProperties
import PathPlanning as path

#Graphs and subgraphs to modify
G = nx.Graph()	#Main graph stores all points able to be visited by a vehicle
P = nx.Graph()	#Temporary graph used to compose seen routes into graph H
H = nx.Graph()	#Used to store all seen points
C = nx.Graph()	#Stores all critical points and the points which they are visible from
routes = []		#Stores nodes along all routes traveled

main_x, main_y = [], []
map.create_map(G)		#initialize entire map

# User input******************************************************************
try:
	opts, args = getopt.getopt(sys.argv[1:], 'gash', ['ground', 'air', 'sea', 'help'])
except getopt.GetoptError:
	print("-g for ground, -a for air, -s for sea")
	sys.exit()

if len(sys.argv) < 2:	 #Check for arguments
		print("-g for ground, -a for air, -s for sea")
		sys.exit()
		
for opt, arg in opts:	#build map based on  options selected by user
	if opt in ('-h', '--help'):
		print("-g for ground, -a for air, -s for sea")
		sys.exit()
		
	elif opt in ('-g', '--ground'):
		map.ground_map(G)		#remove ground obstacles and water from map
		map.var_ground()		#Loads map specific variables

	elif opt in ('-a', '--air'):
		map.air_map(G)			#initialize air map
		map.var_air()			#Loads map specific variables
		
	elif opt in ('-s', '--sea'):
		map.sea_map(G)			#remove Ground area from map leaving only water area
		map.var_sea()			#Loads map specific variables
		
	else:
		sys.exit()

# End user input*******************************************************************

# Path planning loop***************************************************************

for i in range (1):
	
	#get a random route
	patrol_route = path.plan_route(MapProperties.startPoint, G, C, H, MapProperties.crit_points, MapProperties.visDistance, MapProperties.branchStrictness,MapProperties.energyBudget)
	print("Distance traveled in route {0} = {1} ".format (i+1, len(patrol_route)))
	routes = routes + patrol_route
		
	#loop which combines subgraphs along path ab into one large subgraph showing visibility
	for i in range (len(patrol_route)-1):
		xVis, yVis = patrol_route[i]	
		P = nx.ego_graph(G, (xVis,yVis), radius = MapProperties.visDistance, distance = 'weight')
		H = nx.compose (P, H)
		
		
#End of path planning***************************************************************
		
		
#add graph edges to line collection for plotting
lc = mc.LineCollection(G.edges(), color = 'yellow', linewidths = 0.3, linestyles= "--")#anthing done to edges after this will not be displayed
fig, ax = plt.subplots()
ax.add_collection(lc)

#print useful info
print("energy budget =", MapProperties.energyBudget)
print("Critical points are ", MapProperties.crit_points)
if (len(patrol_route) < MapProperties.energyBudget):	
	print ("Route under budget!\nenergy used:\t", len(patrol_route))
else:
	print ("Route over budget!\nenergy used:\t",len(patrol_route))
	
print("{0} out of {1} points seen".format(nx.number_of_nodes(H),nx.number_of_nodes(G)))
	
print("Percent of area seen = ", (math.ceil(nx.number_of_nodes(H)/nx.number_of_nodes(G) * 100)))	
	
print("Total distance traveled =  ", len(routes))
	
#code to show port in background
img = plt.imread('Port.png')
ax.imshow(img, extent=[0,500,0,250])

#plot data into matplotlib graph
plt.scatter(*zip(*list(G.node)), linestyle = ':', marker = "", color = "yellow", alpha = 1)	#Motion
plt.scatter(*zip(*list(H.node)), marker = "8", color = "blue")	#visibility
plt.scatter(*zip(*routes), marker = "D", color = "red")	#route
if MapProperties.crit_points:	#Display crit points if there are any
	plt.scatter(*zip(*MapProperties.crit_points), marker = ",", color = "red", linewidths= 1, edgecolors= "white")


plt.show()

