import heapq

WHITE = (255, 255, 255)

class Planner:
    def __init__(self, surface, world_width, world_height):
        self.surface = surface
        self.world_width = world_width
        self.world_height = world_height

    def heuristic(self, a, b):
        """Returns Manhattan distance"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_path(self, start, goal):
        start = tuple(start)
        goal = tuple(goal)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        open_set = []  # Stores the node to be evaluated
        came_from = {}  # Stores the parent nodes
        heapq.heappush(open_set, (0, start))
        cost = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                break  # Stop when goal is reached

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)

                if 0 <= neighbor[0] < self.world_height and 0 <= neighbor[1] < self.world_width:
                    if self.surface.get_at((neighbor[0], neighbor[1]))[:3] == WHITE:
                        new_cost = cost[current] + 1

                        if neighbor not in cost or new_cost < cost[neighbor]:
                            cost[neighbor] = new_cost
                            priority = new_cost + self.heuristic(neighbor, goal) # cost = heuristic + actual cost from beginning to end
                            heapq.heappush(open_set, (priority, neighbor))
                            came_from[neighbor] = current

        # Reconstruct the path
        path = []
        current = goal
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()

        return path  # Returns empty list if no path is found
