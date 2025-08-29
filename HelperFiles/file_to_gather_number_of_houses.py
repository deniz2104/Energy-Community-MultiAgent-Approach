import random
from enum import Enum

class GatherNumberOfHouses(Enum):
    NUMBER_OF_HOUSES = [1, 5, 10, 15, 20, 23]

    @classmethod
    def get_random_number(cls):    
        return random.choice(cls.NUMBER_OF_HOUSES.value)