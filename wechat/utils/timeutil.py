# -*- coding: utf-8 -*-
import datetime
import time
import random

class TimeUtil():
    def __init__(self, min=3, max=5):
        self.min = min
        self.max = max
    def sleep(self, interval=None):
        if interval:
            time.seep(interval)
        else:
            time.sleep(random.randrange(self.min, self.max))

