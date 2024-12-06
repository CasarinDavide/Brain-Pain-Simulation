
import random
import time
from matplotlib import pyplot as plt
from matplotlib import animation

# Mock function to simulate data generation
class RegrMagic(object):
    def __init__(self):
        self.x = 0
    def __call__(self):
        time.sleep(random.random())  # Simulate a delay
        self.x += 1
        return self.x, random.random()

regr_magic = RegrMagic()

