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
from map_merger import MapMerger
import math

class Pipeline:
	def __init__(self, world_width, world_height, surface):
		# initial position will have to be assumed to be (world_width, world_height)
		self.explored_map1 = Localization(2 * world_width, 2 * world_height) # map explored by agent 1
		self.explored_map2 = Localization(2 * world_width, 2 * world_height) # map explored by agent 2
		self.planner = Planner(world_width, world_height) # gets the path once the map has been finalized
		self.map_merger = MapMerger(2 * world_width, 2 * world_height)
		self.surface = surface
		
		self.path1, self.path2 = None, None

		self.world_height = world_height
		self.world_width = world_width

	def reset(self):
		self.explored_map1 = Localization(2 * self.world_width, 2 * self.world_height) # map explored by agent 1
		self.explored_map2 = Localization(2 * self.world_width, 2 * self.world_height) # map explored by agent 2
		self.path1 = None
		self.path2 = None


	def work(self, agent1, agent2):

		self.explored_map1.update(agent1)
		self.explored_map2.update(agent2)

		# Extracting the local maps
		map1 = self.explored_map1.map.copy()
		map2 = self.explored_map2.map.copy()

		# Merging the maps
		merged_map = self.map_merger.merge_maps(map1, map2)

		self.surface.blit(merged_map, (0, 0))

		# get agent positions
		# pos1 = agent1.get_pos()
		# pos2 = agent2.get_pos()

		# deciding the meeting point
		# meet_x = (pos1[0] + pos2[0]) // 2
		# meet_y = (pos1[1] + pos2[1]) // 2
		# meeting_point = (meet_x, meet_y)

		# generating paths
		# self.path1 = self.planner.get_path(merged_map, (pos1[0], pos1[1]), meeting_point)
		# self.path2 = self.planner.get_path(merged_map, (pos1[0], pos1[1]), meeting_point)

		# print('path 1 : ', self.path1)
		# print('path 2 : ', self.path2)

		# # Move agents through the planned path
		# self.move_agent(agent1, self.path1)
		# self.move_agent(agent2, self.path2)

	def move_agent(self, agent, path):

		step_size = 3

		for i in path:
			agent.move(step_size)
			pos = agent.get_pos()
			rotate_angle = math.atan((i[1] - pos[1]) / (i[0] - pos[0]))
			rotate_angle = math.degrees(rotate_angle)
			agent.rotate(rotate_angle)

        

		

