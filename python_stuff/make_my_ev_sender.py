# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:57:03 2015

@author: Johan
"""


# a class that sends events regardless of attached device. So that during my experiment, I don't
# have to worry aobut that - the abstraction lies in here.

# written on-the-fly. So abstractions are right now something to improve upon.
# like: where do I do my device-specific stuff, do I make own functions for them, and where?
# right now I opted to have it distributed into the class itself, while in prinicple,
# it's nicer to maybe even make sub-classes per device for easy implementation later on.
# hmm - maybe I shoudl do this anyway. Damn.

# let's see how much the quick-n-dirty class implementation method of work would be
# improved by using python and NOT matlab - the king of quick n dirty.


# stuff we beed to send stuff:
import egi.simple as egi
# import parallel
import threading

import time

# fill in later to allow me to send BP triggers via parallel.
# most easy now - i just need to take care to instantiate the right object.
# and THEN - I just use init, send and finish!!
# maybe I could even make a super-class of this.
# but not.. now..
class brain_products_sender():
    def __init__(self):
        pass
    
    def init(self):
        pass
    
    def send(self,ev):
        pass
    
    def finish(self):
        pass
    

# this looks a little bit cleaner, already - i can focus just on one class if i wish
# to implement another recorder.
class egi_sender():
    def __init__(self):
        pass
        
    def init(self):
        ns = egi.Netstation()
        ns.connect('10.0.0.42', 55513) # sample address and port -- change according to your network settings            
        ns.BeginSession()     
        ns.sync()     
        ns.StartRecording()
        # save it to obj namespace for later use.
        self.ns=ns
        
    def send(self,ev):
        ns = self.ns
        # so - if you say 0 (i.e., the number, then EGI will just make it a string - easy.)
        # would make more sense within an inheritance model - or NOT, in this case.
        # because ONLY for EGI do you wish for a string.
        if not isinstance(ev,str):
            ev = str(ev)

        timestamp = egi.ms_localtime()
        
        ns.send_event( ev, label=ev, timestamp=timestamp, table = {'label' : ev, 'timestamp' : timestamp} ) 
        
    def finish(self):
        ns = self.ns
        ns.StopRecording()
        ns.EndSession()
        ns.disconnect()


# the MAIN class: ev_sender!
class ev_thread(threading.Thread):
    
    # init asks you for what kind of device you have attached
    # it also inits for you - if needed
    def __init__(self,sender_obj):
        # overload..
        threading.Thread.__init(self)
        # output_device can be either:
        # 'no_device'
        # 'egi'
        # 'brain_products'
        # !!! instantiate THIS object with a sender object!
        self.sender = sender_obj
        self.ev_list=[]
        # for clean exit
        self.stop_sending = 0
        # do the init stuff separately (necessary) - makes you work for it
        self.sender.init()

        
    def run(self):

        # apply the LIFO rule for sending events.
        while len(self.ev_list)>0:

            # pop it..
            ev=self.ev_list.pop(0)

            # send it!
            self.sender.send(ev)
            
            # arrange for a clean exit
            if self.stop_thread == 1:
                # disconnect, etc etc:
                self.sender.stop()
                # then - exit this loop.
                break
            
            # make sure the processor doens't take it all up!
            # allow for 1 msec time inaccuracy, too.
            time.sleep(0.001)


    def send(self,ev):
        # just append it to the list - so it'll be taken off in the main while loop.
        self.ev.append(ev)
        
        
    def stop(self):
        self.stop_thread = 1
        