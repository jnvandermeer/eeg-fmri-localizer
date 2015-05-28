# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:03:35 2015

@author: Johan
"""

# >>> send many events here >>> 

 
## # optionally can perform additional synchronization     

## ns.sync()     

if EGI_CONNECTED:
    ns.send_event( 'evt_', label=str(Go_Nogo)+"-"+str(LR), timestamp=egi.ms_localtime(), table = {'label' : label, 'fld2' : "abc", 'fld3' : 0.042} ) 
    
import egi.simple as egi

## import egi.threaded as egi

 

# ms_localtime = egi.egi_internal.ms_localtime     

ms_localtime = egi.ms_localtime     

 

EGI_CONNECTED=0

if EGI_CONNECTED:

    ns = egi.Netstation()

    ns.connect('10.0.0.42', 55513) # sample address and port -- change according to your network settings

    ## ns.initialize('11.0.0.42', 55513)

    ns.BeginSession()     

     

    ns.sync()     

     

    ns.StartRecording()

     
