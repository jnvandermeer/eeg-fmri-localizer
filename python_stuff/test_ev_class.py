# -*- coding: utf-8 -*-
"""
Created on Thu May 28 18:49:54 2015

@author: Johan
"""
import threading
import time

# use this nice 'dummy' class! - so that u have the object, but it doesn't do anything.
class none_sender():
    def __init__(self):
        pass
    
    def init(self):
        print('none_sender: INITIALIZED')
    
    def send(self,ev):
        print(ev)
        # for me a print; normally:
        pass
    
    def finish(self):
        print('none_sender: DISCONNECT/STOPPED')
    


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
        threading.Thread.__init__(self)
        # output_device can be either:
        # 'no_device'
        # 'egi'
        # 'brain_products'
        # !!! instantiate THIS object with a sender object!
        self.sender = sender_obj
        self.ev_list=[]
        
        
        # do the init stuff separately (necessary) - makes you work for it
        self.sender.init()
        
        # for clean exit
        self.stop_thread = 0

        
    def run(self):


        # keep on doing this - unless the stop signal has been given.
        while True:

            # check if there's something in the ev_list - resolve those
            # then - continue.
            if len(self.ev_list)>0:
                while len(self.ev_list)>0:
        
                    # pop it..
                    # apply the LIFO rule for sending events.
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
        self.ev_list.append(ev)
        
        
    def stop(self):
        self.stop_thread = 1