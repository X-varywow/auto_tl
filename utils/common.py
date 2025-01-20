import random
import time

# 0.1 -> -0.1 ~ 0.1
def get_random(ratio):
    return (random.random()-0.5)*ratio*2

def random_sleep(t, roll = 0.1):
    time.sleep(t*(1+get_random(roll)))