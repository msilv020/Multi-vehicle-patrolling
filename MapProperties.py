# Variables used throughout the program.
#  default values
startPoint = (0,0)
visDistance = 3			#visibility range = visDistance * 5
energyBudget = 112 		#the diagonal of the graph = 559 rounded to 560
crit_points = []	    #points that should be checked on patrol if possible
branchStrictness = 0.5 	#Top percentage of furthest nodes that path points are selected from
						#(lower value increases loop length but reduces potential path candidates) since energy budget is fixed
