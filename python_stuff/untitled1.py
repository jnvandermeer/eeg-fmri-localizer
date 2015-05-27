# -*- coding: utf-8 -*-
"""
Created on Tue May 26 20:10:52 2015

@author: Johan
"""

import time
import threading
import random


def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]
    

class letter_stream(threading.Thread):
    def __init__(self,letters,switch_frequency,switch_probability):
        threading.Thread.__init__(self)

        self.letters=letters
        self.flag = 0
        self.switch_frequency=switch_frequency
        self.switch_probability = switch_probability
        self.isstarted=0
        self.current_letter='X'
        self.stop = 0


    def run(self):
        print('started letter thread...')
        self.isstarted=1
        start_time=time.time()

        letters=self.letters
        switch_frequency=self.switch_frequency
        switch_probability=self.switch_probability


        cal_time = time.time()
        # keep on doing this - until the end of the experiment, when I 'quit' the CORE:
        while True:

            # if the time bigger than the 'cal' time:
            if time.time() - cal_time > 0:
                # effecively, only run this code-block once every letter_time_interval:
                cal_time = cal_time + switch_frequency
                # switch the letter - according to the given chance:
                if random.random() < switch_probability:
                    letters = shift(letters,-1)
                else:
                    letters = shift(letters,1)
                # set the 'current' letter.
                self.current_letter = letters[0]
                # set the flag, too.
                self.flag = 1
            
            # sleep - for only a short time.
            time.sleep(0.01)
    
            if self.stop:
                break



    def getLetter(self):
        return self.current_letter

    def isStarted(self):
        return self.isstarted

    def queryFlag(self):
        if self.flag==1:
            self.flag = 0
            return 1
        else:
            return 0

    def setStop(self):
        self.stop=1
