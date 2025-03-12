import pygame
import math

WHITE = (255, 255, 255)

class Localization:
    def __init__(self, world_width, world_height):
        self.map = pygame.Surface((world_width, world_height)) 
        self.map.fill((0, 0, 0))
        self.__world_height = world_height
        self.__world_width = world_width

        # # random guess about the agent's position (x, y, angle)
        # self.position = [0, 0, 0]

        self.position = None

    def update(self, agent):

        agent_angle = agent.get_imu_data() # angle of the agent

        lidar_readings = agent.scan() # gets the lidar readings
        
        if self.position == None:
            self.position = agent.get_pos()

        for distance in lidar_readings:
            if distance > 0:
                rad_angle = math.radians(agent_angle)

                obs_x = int(self.position[0] + (distance * math.cos(rad_angle)))
                obs_y = int(self.position[1] + (distance * math.sin(rad_angle)))

                self.map.set_at((obs_x, obs_y), WHITE) # Set an obstacle at this position

            agent_angle += 2

        # for i in range(0, 360, 2):
        #     distance = lidar_readings[i//2]
        #     if distance > 0:
        #         rad_angle = math.radians(i)
        #         obstacle_x, obstacle_y = distance * math.cos(agent_angle + rad_angle), distance * math.sin(agent_angle + rad_angle)

        #         obstacle_x = int(obstacle_x)
        #         obstacle_y = int(obstacle_y)
                
        #         self.map.set_at((obstacle_x, obstacle_y), WHITE) # Set an obstacle at this position

    def get_pos(self):
        return self.position


    
    def at(self, x, y):
        return self.map.get_at((int(x), int(y)))

