import pygame
import numpy as np

class MapMerger:
    def __init__(self, world_width, world_height):
        self.__map = None

    def merge_maps(self, map1, map2):
        self.__map = np.maximum(map1.slam.get_estimated_map(), map2.slam.get_estimated_map())
        return self.__map