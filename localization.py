import pygame
import random
import numpy as np
import math

WHITE = (255, 255, 255)
BROWN = (181, 101, 29)

# Particle filtering is used for determining the location of agents given the world map

class Localization:
    def __init__(self, world_width, world_height, map_data, num_particles = 150):
        self.world_width = world_width
        self.world_height = world_height
        self.num_particles = num_particles
        self.map_data = map_data
        self.particles = self.initialize_particles()

    def initialize_particles(self):  # randomly intializing particles all over the map
        particles = []
        for i in range(self.num_particles):
            pos = (random.randrange(0, self.world_width), random.randrange(0, self.world_height))
            while self.map_data.get_at(pos) == BROWN:
                pos = (random.randrange(0, self.world_width), random.randrange(0, self.world_height))
            
            particles.append(pos)
        
        return particles
    
    def move_particles(self, agent_motion):
        """
        Move particles based on the motion of the agent
        """
        dl, theta = agent_motion
        dx = dl * math.cos(theta)
        dy = dl * math.sin(theta)

        for i in range(self.num_particles):
            new_x = int(self.particles[i][0] + dx)
            new_y = int(self.particles[i][1] + dy)
            if 0 < new_x < self.world_width and 0 < new_y < self.world_height and self.map_data.get_at((new_x, new_y)) == WHITE:
                self.particles[i] = (new_x, new_y)

    def update(self, agent):
        """
        Update particle weights based on lidar readings
        """
        lidar_data = agent.scan()
        weights = np.zeros(self.num_particles)
        angle = agent.get_imu_data()

        for i in range(self.num_particles):
            x, y = self.particles[i]
            simulated_lidar = self.simulate_lidar(x, y, angle)
            print("lidar data : ", lidar_data)
            print("simulated lidar data : ", simulated_lidar)
            weights[i] = np.exp(-np.sum((simulated_lidar - lidar_data) ** 2) / 1e7) # weights based on the simulated reading the actual lidar readings for each particle

        print("weigths : ", weights)
        weights /= np.sum(weights) # Normalize weights
        self.resample(weights)

    def resample(self, weights):
        """
        Resamples particles based on their weights
        """
        new_particles = []
        idxs = np.random.choice(self.num_particles, size = self.num_particles, p = weights)
        noise = 40

        i = 0
        while len(new_particles) < self.num_particles:
            new_particles.append(self.particles[idxs[i]])

            # randomly assigning new particles around the above index
            num_more_particles = random.randrange(0, 11)
            for _ in range(num_more_particles):
                x = random.randrange(self.particles[idxs[i]][0] - noise, self.particles[idxs[i]][0] + noise)
                y = random.randrange(self.particles[idxs[i]][1] - noise, self.particles[idxs[i]][1] + noise)
                new_particles.append((x, y))
            
            i += 1


        self.particles = new_particles

    def get_estimated_pos(self):
        """
        Returns mean of the particles as the estimated agent's position
        """
        return np.mean(self.particles, axis = 0).astype(int)

    
    def simulate_lidar(self, x, y, angle, fov = 360, resolution = 2):  # for simulating lidar same as that of robot_api.py

        num_rays = int(fov / resolution)
        start_angle = angle - fov / 2.0
        measurements = []
        for i in range(num_rays):
            ray_angle = start_angle + i * resolution
            ray_angle_rad = math.radians(ray_angle)
            d = self.__raycast(x, y, ray_angle_rad)
            measurements.append(d)
        
        return np.array(measurements)
    
    def __raycast(self, x, y, angle_rad):  # for simulating lidar same as that of robot_api.py
        step = 1.0
        distance = 0.0

        while distance < self.world_width:
            test_x = x + distance * math.cos(angle_rad)
            test_y = y + distance * math.sin(angle_rad)
            ix, iy = int(test_x), int(test_y)
            if ix < 0 or iy < 0 or ix >= self.world_width or iy >= self.world_height:
                return self.world_width
            if self.map_data.get_at((ix, iy))[:3] == BROWN:
                return distance
            distance += step
        return self.world_width

