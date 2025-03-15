"""
API for agent: (Read robot_api.py for more detailed documentation)
agent.move(dist)     : moves the agent in forward direction for dist units. Avoid using values more than 5 the value of distance for one 
					   iteration of work. It will still work but you won't see it being animated (was too much effort implementing that)
agent.scan()         : returns a list of size 180 which gives distance of nearest obstacle/wall for every 2 degrees 
						with 0th element being the distance at degree the agent is facing - 180
agent.rotate(deg)    : rotates the agent by deg degrees
agent.get_imu_data() : gives the direction the agent is heading towards.

(For Subtasks)
agent.get_world() :  gives pygame.Surface of the world, if this.get_at((x, y)) != WHITE then its a wall
agent.get_pos()   : returns coordinates of the agent. Usable only once. (x, y) = (pos[0], pos[1])

Task : This class is supposed to make the two agents meet somewhere on the map. You can create the map yourself in the pygame GUI, you can
save and load maps from your system. Your code will be tested on different maps which I will make randomly lol. You are 
supposed to document your progress. Your approach and effort to solve this problem matters more than the final solution. 
One approach to solve this is to implement localization and mapping to get the map for both agents and then use some kind of map merging algorithm 
to get a transform between the maps and use that to get relative displacement between the two agents and use that to make them meet. Subtasks 
given below are supposed to reduce the number of things you need to do make the agents meet. You can use any resource (pre-written code, LLMs, 
books etc) but you are supposed to mention what you used in your documentation and have a basic understanding of what you did. 

Subtask 1: You can use initial coordinates of both agents and the world surface map
Subtask 2: In conditions of subtask 1, ensure a smooth path. Read about Dubin Curves or Reeds-Shepp
Subtask 3: You can use initial coordinates of both agents but not the map
Subtask 4: You can use the map but not coordinates of either of agents
Subtask 5: You can use only scan and imu data.

Subtask 6 (Bonus): Do this optimally without scanning the full map if possible. (Some image processing techniques may be used)

If you do Subtask x, you get points for all Subtask y such that y <= x

GUI:
You can use WASD and arrow keys to control the agents. It will be helpful in debugging (or you can just play around lol)
Add Walls : duh, it adds walls. You can use a brush to add walls to the map.
Remove Walls : You can use a brush to remove walls from the map.
Start Pipeline : It basically runs the work function in this class
View : There are two views 
		Full -> in this mode the normal map with brown walls and white background is shown
		Explored -> this shows the area that the scan has explored till now in white color rest is in black
Upload Map : This can be used to upload a .png file as map. Note: stuff might get buggy if you upload something that you didn't save from the GUI but essentially anything with brown rgb(181, 101, 29) walls and white backgruond should work. 
Save Map : This saves the current map as a .png file. 

Note: If you find any bugs, try to fix them and write about them in your documentation and DM me (aryanr_) on discord
"""

from localization import Localization
from planning import Planner
import random
import pygame

class Pipeline:
	def __init__(self, world_width, world_height, surface, agent1, agent2):

		# map data for agents
		self.__map_data1 = agent1.get_world()
		self.__map_data2 = agent2.get_world()

		self.__world_width = world_width
		self.__world_height = world_height
		self.surface = surface

		self.explored_map1 = Localization(world_width, world_height, self.__map_data1) # map explored by agent 1
		self.explored_map2 = Localization(world_width, world_height, self.__map_data2) # map explored by agent 2
		self.planner = Planner(self.__map_data1, world_width, world_height) # gets the path once the map has been finalized

		# random guess for the initial positions
		self.pos1 = self.explored_map1.get_estimated_pos()
		self.pos2 = self.explored_map2.get_estimated_pos()

		# connecting path
		self.path = None

		# other variables regarding the movement of agents
		self.__steps_moved = 0
		self.__max_steps = 20
		self.__min_step_size = 5
		self.__max_step_size = 20


	def reset(self, agent1, agent2):

		self.__map_data1 = agent1.get_world()
		self.__map_data2 = agent2.get_world()

		self.explored_map1 = Localization(self.__world_width, self.__world_height, self.__map_data1) # map explored by agent 1
		self.explored_map2 = Localization(self.__world_width, self.__world_height, self.__map_data2) # map explored by agent 2
		self.pos1 = self.explored_map1.get_estimated_pos()
		self.pos2 = self.explored_map2.get_estimated_pos()
		self.path = None
		self.__steps_moved = 0


	def work(self, agent1, agent2):

		if self.__steps_moved < self.__max_steps:
			
			# making the agent do some motion to determine the surrounding map
			agent1_motion = self.move_agent(agent1)
			agent2_motion = self.move_agent(agent2)

			# moving the randomly initialized particle and updating their weights
			self.explored_map1.move_particles(agent1_motion)
			self.explored_map1.update(agent1)
			
			self.explored_map2.move_particles(agent2_motion)
			self.explored_map2.update(agent2)

			# estimated new position
			self.pos1 = self.explored_map1.get_estimated_pos()
			self.pos2 = self.explored_map2.get_estimated_pos()

			self.__steps_moved += 1

			print(self.__steps_moved)

		else:

			if not self.path: 
				print(agent1.get_pos(), agent2.get_pos()) # can be used only once! real locations
				print(self.pos1, self.pos2) # estimated locations

				self.path = self.planner.get_path(self.pos1, self.pos2 ) # apply astar to make path between the two estimated locations for both agents
				print(self.path)

				if len(self.path) == 0:
					print("Agent cannot meet each other")

				for i in range(1, len(self.path)):  # drawing the path
					pygame.draw.line(self.surface, (255, 0, 0), self.path[i - 1], self.path[i])

	
	def move_agent(self, agent):  # making random movement for the agent
		dl = random.randrange(self.__min_step_size, self.__max_step_size + 1)
		dtheta = random.uniform(0, 360)
		agent.rotate(dtheta)
		agent.move(dl)

		return dl, dtheta