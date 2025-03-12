import pygame
import heapq

BROWN = (181, 101, 29) 

class Planner:
    def __init__(self, world_width, world_height):
        self.__world_width = world_width
        self.__world_height = world_height

    def get_dis(self, a, b):
        """ Returns manhattan distance """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def is_free_space(self, surface, x, y):
        x = int(x)
        y = int(y)
        if surface.get_at((x, y)) == BROWN:
            return False
        return True

    def get_path(self, surface, start, goal):
        """ A* pathfinding algorithm to get path """

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        open_set = [] # to be evaluted
        closed_set = {} # already evaluted
        heapq.heappush(open_set, (0, start))
        cost = {start : 0}

        while len(open_set) : 
            _, current = heapq.heappop(open_set)

            if current == goal : 
                break

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)

                if 0 <= neighbor[0] <= self.__world_width and 0 <= neighbor[1] <= self.__world_height:
                    # check if space is free, if free and neighbor not in closet set then add to f cost and compute cost and do do and find path
                    if self.is_free_space(surface, neighbor[0], neighbor[1]) :
                        new_cost = cost[current] + 1

                        if neighbor not in closed_set or new_cost < cost[neighbor]:
                            cost[neighbor] = new_cost
                            priority = new_cost + self.get_dis(neighbor, goal)
                            heapq.heappush(open_set, (priority, neighbor))
                            closed_set[neighbor] = current

        
        ans = []
        current = goal
        while current in closed_set:
            ans.append(current)
            current = closed_set[current]
        ans.reverse()
        return ans
