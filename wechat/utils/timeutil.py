# -*- coding: utf-8 -*-
import time, random

class TimeUtil():
    def __init__(self, min=3, max=10):
        self.min = min
        self.max = max
    def sleep(self, interval=None):
        if interval:
            time.sleep(interval)
        else:
            time.sleep(random.randrange(self.min, self.max))


