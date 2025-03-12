import pygame, numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class MapMerger:
    def __init__(self, world_width, world_height):
        self.__map = pygame.Surface(( world_width, world_height))
        self.__map.fill(BLACK)

    def merge_maps(self, map1, map2):

        map1_arr = pygame.surfarray.array3d(map1)
        map2_arr = pygame.surfarray.array3d(map2)

        merged_map = np.maximum(map1_arr, map2_arr) # Overlay the two maps

        pygame.surfarray.blit_array(self.__map, merged_map) # copy the merged_map to self.__map

        return self.__map
