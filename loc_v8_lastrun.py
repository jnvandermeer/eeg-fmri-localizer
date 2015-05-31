#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.82.01), mei 29, 2015, at 14:34
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'loc_v1'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\Rachel Koops\\Desktop\\Vis_mot_inh_taak\\EEG\\eeg-fmri-localizer\\loc_v8.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1600, 900), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "ask_for_size"
ask_for_sizeClock = core.Clock()
text_ask_for_version = visual.TextStim(win=win, ori=0, name='text_ask_for_version',
    text="What size of Stimuli?\n\n1) Normal Size (100%)\n2) Smaller Size (75%)\n3) Even Smaller (50%)\n4) Smallest Size (25%)\n5) Doesn't fit on screen (125%)\n6) Even worse fit (150%)",    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)


# Initialize components for Routine "do_video"
do_videoClock = core.Clock()
import time
import threading
import copy


# control whether we will do single or double checkerboard flips:
global vis_do_double_flip
vis_do_double_flip = False

# control whether we will do the other side too, with freq of 0.4 Hz - to avoid ghosting artifact in yoru eye.
# global vis_flip_other_side
vis_flip_other_side = True
vis_flip_other_side_interval = 2.5 # this many seconds pass untill the otherside's contrast is flipped.

# initiate my visual stimuli:
vis_times={'8':[0.001,0.111, 0.253,0.373,0.475, 0.600],'13':[0.001,0.078,0.151,0.214,0.300,0.376,0.442,0.525,0.600]}

# so these are the individual STIMS (which we don't have for audio)
visual_evt_codes={'left':{'8':87,'13':137},'right':{'8':88,'13':138}}

# these are markers for the frequency analysis
visual_evt_codes_begin={'left':{'8':83,'13':133},'right':{'8':84,'13':134}}
visual_evt_codes_end={'left':{'8':85,'13':135},'right':{'8':86,'13':136}}

# these are the thread starts - which conveniently also denotify what your visual segments
# should BE - in case you wish to reconstruct the visual ERP
global visual_evt_codes_beginvisthread
visual_evt_codes_beginvisthread={'left':{'8':81,'13':131},'right':{'8':82,'13':132}}


# for audio - we need to actually insert ADDITIONAL markers denotifying the start and end of each segment.
# AND (!) also denotify the start and end of each click - but this will be done later in MATLAB. I guess.
# we need to find the correct sequence, for this. 
# reconstruct these from the MATLAB data.


class play_vis_stim(threading.Thread):
    def __init__(self,vis_times,side,freq,evt):
        threading.Thread.__init__(self)
        self.win=win
        # is this it?
        self.hit_times=copy.deepcopy(vis_times[freq])
        self.side=side
        self.flash=0
        self.isstarted=0
        self.freq = freq

        print self.side
        print self.freq


    def run(self):

        print('started visual thread...')
        side=self.side
        freq=self.freq
        self.isstarted=1
        # get the list
        hit_times = self.hit_times
        # this is to make things run/work
        max_time = hit_times[-1]
        hit_times[-1] = -1

        start_time=time.time()
        target_time = hit_times.pop(0)
        evt.send(visual_evt_codes_beginvisthread[side][freq])

        while True:
            current_time = time.time() - start_time
            if current_time >target_time and target_time > 0:
    
                #print current_time
                #print target_time
                #print 'flashed'

                self.flash=1;

                # get us a NEW target time !!
                target_time = hit_times.pop(0)

            if current_time>max_time:
                #print 'broke while loop at time = %f ' % current_time
                break
    
            time.sleep(0.0005)

    def resetFlash(self):
        self.flash=0

    def queryFlash(self):
        return self.flash

    def getSide(self):
        return self.side

    def isStarted(self):
        return self.isstarted

    def getFreq(self):
        return self.freq

# Initialize components for Routine "do_audio"
do_audioClock = core.Clock()
import threading
import time


# define my dict.
sounds={'left':{'40':sound.Sound('stim/audio_40Hz_L.wav', secs=-1),'55':sound.Sound('stim/audio_55Hz_L.wav', secs=-1)},'right':{'40':sound.Sound('stim/audio_40Hz_R.wav', secs=-1),'55':sound.Sound('stim/audio_55Hz_R.wav', secs=-1)}}

# initiate my volumes...
sounds['left']['40'].setVolume(1)
sounds['right']['40'].setVolume(1)
sounds['left']['55'].setVolume(1)
sounds['right']['55'].setVolume(1)

# for later, too.
audio_evt_codes={'left':{'40':41,'55':51},'right':{'40':42,'55':52}}
audio_evt_codes_begin={'left':{'40':43,'55':53},'right':{'40':44,'55':54}}
audio_evt_codes_end={'left':{'40':45,'55':55},'right':{'40':46,'55':56}}


class play_audio_stim(threading.Thread):
    def __init__(self,sounds,side,freq,evt):
        threading.Thread.__init__(self)
        self.side=side
        self.freq=freq
        self.sounds=sounds
        self.isstarted=0

    def run(self):
        print('started audio thread...')
        self.isstarted=1
        start_time=time.time()
        sounds=self.sounds
        freq=self.freq
        side=self.side

        # send the code here to external device using my own object - then proceed by playing the sound
        evt.send(audio_evt_codes[side][freq])


        # current_time = time.time() - start_time
        # print current_time
        my_sound = sounds[side][freq]
        my_sound.play()
        # ... aaand... we neatly wait untill the sound has been finished!
        time.sleep(my_sound.getDuration())
        current_time = time.time() - start_time
        print '---'
        print current_time

        
    def isStarted(self):
        return self.isstarted

    def getSide(self):
        return self.side

    def getFreq(self):
        return self.freq

# Initialize components for Routine "do_letters"
do_lettersClock = core.Clock()


# Initialize components for Routine "do_triggers"
do_triggersClock = core.Clock()
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:57:03 2015

@author: Johan
"""
# this is all I need to make my experiment output some triggers.
# USAGE (very simple):

# check the sender objects - use the one appropriate!
# then - instantiate an ev_thread - give as agurment an instantiation of the appropriate sender object.

#   evt = evt_thread(egi_sender())

# then  start it:

#   evt.start()

# then - send events like so (i.e., strings!)
# brain products DOES wish only for INTs, though. That sort of sucks, given that EGI accepts strings. Naja. Implement it anyway.

#   evt.send(10)

# finally, at the end of the experiment  - stop it

#   evt.stop()


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


# use this nice 'dummy' class! - so that u have the object, but it doesn't do anything.
class none_sender():
    def __init__(self):
        pass
    
    def init(self):
        print('none_sender: INITIALIZED')
    
    def send(self,ev):
        # print('none_sender: sending: ' + str(ev))
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
        print('egi_sender: INITIALIZED')

    
    def send(self,ev):
        ns = self.ns
        ev=str(ev)
        print('egi_sender: sending: ' + str(ev))
        timestamp = 0.
        ns.send_event( ev, label=ev, timestamp=egi.ms_localtime(), table = {'fld1' : ev} ) 
        #ns.send_event( 'evt_', label=str(ev), timestamp=timestamp, table = {'label' : str(ev), 'timestamp' : timestamp} ) 
        
    def finish(self):
        ns = self.ns
        ns.StopRecording()
        ns.EndSession()
        ns.disconnect()
        print('egi_sender: DISCONNECT/STOPPED')




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
        
        # for clean exit - set to 0 now, of course.
        self.stop_thread = 0


    # so what should this thread do??
    # -- ! just remain on the background at all times.
    # as event handler, I can also try to implement a text thingy.
    # then I can yield a LIST of output modalities
    # ... if asked for this.
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
                self.sender.finish() # yes - well, I don't call it stop, just to be totally tegendraads.
                # then - exit this loop.
                break
            
            # make sure the processor doens't take it all up!
            # allow for 1 msec time inaccuracy, too.
            time.sleep(0.0005)

    def send(self,ev):
        # just append it to the list - so it'll be taken off in the main while loop.
        self.ev_list.append(ev)
        
        
    def stop(self):
        self.stop_thread = 1
select_eeg_system = visual.TextStim(win=win, ori=0, name='select_eeg_system',
    text="What is your EEG system?\n\n1) Nothing (don't send triggers)\n\n2) EGI\n\n3) Brain Products",    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)


# Initialize components for Routine "instr"
instrClock = core.Clock()

instr_text = visual.TextStim(win=win, ori=0, name='instr_text',
    text='Mind the numbers in the middle\n\nIf the sequence changes:\n\npress a key!',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Initialize components for Routine "main_routine"
main_routineClock = core.Clock()



# Initialize components for Routine "end"
endClock = core.Clock()
end_text = visual.TextStim(win=win, ori=0, name='end_text',
    text='This was the end - Thank you!',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)


# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "ask_for_size"-------
t = 0
ask_for_sizeClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
get_size_key = event.BuilderKeyResponse()  # create an object of type KeyResponse
get_size_key.status = NOT_STARTED

# keep track of which components have finished
ask_for_sizeComponents = []
ask_for_sizeComponents.append(text_ask_for_version)
ask_for_sizeComponents.append(get_size_key)
for thisComponent in ask_for_sizeComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "ask_for_size"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = ask_for_sizeClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_ask_for_version* updates
    if t >= 0.0 and text_ask_for_version.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_ask_for_version.tStart = t  # underestimates by a little under one frame
        text_ask_for_version.frameNStart = frameN  # exact frame index
        text_ask_for_version.setAutoDraw(True)
    
    # *get_size_key* updates
    if t >= 0.0 and get_size_key.status == NOT_STARTED:
        # keep track of start time/frame for later
        get_size_key.tStart = t  # underestimates by a little under one frame
        get_size_key.frameNStart = frameN  # exact frame index
        get_size_key.status = STARTED
        # keyboard checking is just starting
        get_size_key.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if get_size_key.status == STARTED:
        theseKeys = event.getKeys(keyList=['1', '2', '3', '4', '5', '6', 'space', 'escape'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            get_size_key.keys = theseKeys[-1]  # just the last key pressed
            get_size_key.rt = get_size_key.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in ask_for_sizeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "ask_for_size"-------
for thisComponent in ask_for_sizeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if get_size_key.keys in ['', [], None]:  # No response was made
   get_size_key.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('get_size_key.keys',get_size_key.keys)
if get_size_key.keys != None:  # we had a response
    thisExp.addData('get_size_key.rt', get_size_key.rt)
thisExp.nextEntry()

# VERY exhaustive - can i do this better?
my_key_pressed = get_size_key.keys
stimuli_sizes = {'1':1.00, '2':0.75,'3':0.50,'4':0.25,'5':1.25,'6':1.50} # of course it is a comma - like everything in pyhton
SIZE_MUL_FACTOR = stimuli_sizes[my_key_pressed]

# the Routine "ask_for_size" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "do_video"-------
t = 0
do_videoClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
#for i in range(0,100):
 #   if i==0:
  #      p1=play_vis_stim(win, hit_times_8Hz, right_cb,left_cb,fixation,'left')
   #     p1.run()
    #time.sleep(0.1)

#p2=play_vis_stim(win, hit_times_8Hz, right_cb,left_cb,fixation,'right')
#p2.start()

#p3=play_vis_stim(win, hit_times_13Hz, right_cb,left_cb,fixation,'left')
#p3.start()
#p4=play_vis_stim(win, hit_times_13Hz, right_cb,left_cb,fixation,'right')
#p4.start()


# keep track of which components have finished
do_videoComponents = []
for thisComponent in do_videoComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "do_video"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = do_videoClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in do_videoComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "do_video"-------
for thisComponent in do_videoComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "do_video" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "do_audio"-------
t = 0
do_audioClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
# a = play_audio_stim(sounds,'right',55)
# a.start()

# keep track of which components have finished
do_audioComponents = []
for thisComponent in do_audioComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "do_audio"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = do_audioClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in do_audioComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "do_audio"-------
for thisComponent in do_audioComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "do_audio" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "do_letters"-------
t = 0
do_lettersClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
text_stim = visual.TextStim(win=win, ori=0, name='text_4',
    text='0',    font=u'Arial',
    pos=[0, 0], height=0.1*SIZE_MUL_FACTOR, wrapWidth=None,
    color=u'red', colorSpace='rgb', opacity=1,
    depth=0.0)

# txt event codes - declaration
txt_evt_codes = {'normal':100, 'oddball':101}

# quick and dirty shift function. Matlab has got its own built-in 'circshift' - I need to do it like this, now.
import random # if I didn't , already! - or if psychopy didn't , already.
def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

# doesn't matter if it's a set or if it's a list, for our purposes
# letters_for_letter_stream = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# letters_for_letter_stream = [x.upper() for x in letters_for_letter_stream]
letters_for_letter_stream = ['0','1','2','3','4','5','6','7','8','9']
# list comprehension uppercase trick:


# another thing to think about: setting a 'DEFAULT' input parameter (like NONE?) - how to do that?
# the letter_stream could be done better and made more general. Now it's too focussed on 'letters', but it should be really focussed on 'characters' or 'strings', or whatever kind of elements may be.
# the only thing is - in psychopy, it's not that easy to search-and-replace. In matlab it would've been quicker (for now). Program it in Spyder.. seems to be interesting!

class letter_stream(threading.Thread):
    def __init__(self,letters,switch_frequency,switch_probability,evt):
        threading.Thread.__init__(self)

        self.letters=letters
        self.flag = 0
        self.switch_frequency=switch_frequency
        self.switch_probability = switch_probability
        self.isstarted=0
        self.current_letter='0'
        self.stop = 0
        self.type = 'normal'


    def run(self):
        print('started letter thread...')
        self.isstarted=1
        start_time=time.time()

        letters=self.letters
        switch_frequency=self.switch_frequency
        switch_probability=self.switch_probability


        cal_time = time.time()+switch_frequency # prevent from jumping the first later - irritating!
        # keep on doing this - until the end of the experiment, when I 'quit' the CORE:
    
        # beauty fix - start 1 sec after start of the experiment
        time.sleep(1.0)

        # somehow control that things don't go too fast (effectively reduces the % change of an oddball occurring
        lastoddball = 0 # set counter to 0
        new_lim = 4 # make sure no oddball happens IMMEDEATELY into the experiment:
        letter_direction = 1; # oddball = reverse letter direction

        while True:
            # if the time bigger than the 'cal' time:
            if time.time() - cal_time > 0:
                # effecively, only run this code-block once every letter_time_interval:
                cal_time = cal_time + switch_frequency
                # switch the letter - according to the given chance:
                if random.random() < switch_probability and lastoddball > new_lim:
                    # make a (randomly chosen) ISI where nothing should happen.
                    new_lim = 1+round(random.random()*3+2) # between 3 and 6 = the ISI - at LEAST
                    lastoddball = 0
                    letter_direction = letter_direction*-1
                    # letters = shift(letters,-1)
                    self.type = 'oddball'
                else:
                    lastoddball = lastoddball + 1
                    self.type = 'normal'

                letters = shift(letters,letter_direction) # well - to be true - it's ONLY the direction that counts, not the size. Like Vector in Dispicable Me.
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

    def getType(self):
        return self.type
# keep track of which components have finished
do_lettersComponents = []
for thisComponent in do_lettersComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "do_letters"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = do_lettersClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in do_lettersComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "do_letters"-------
for thisComponent in do_lettersComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "do_letters" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "do_triggers"-------
t = 0
do_triggersClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat

eeg_resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
eeg_resp.status = NOT_STARTED

# keep track of which components have finished
do_triggersComponents = []
do_triggersComponents.append(select_eeg_system)
do_triggersComponents.append(eeg_resp)
for thisComponent in do_triggersComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "do_triggers"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = do_triggersClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # *select_eeg_system* updates
    if t >= 0.0 and select_eeg_system.status == NOT_STARTED:
        # keep track of start time/frame for later
        select_eeg_system.tStart = t  # underestimates by a little under one frame
        select_eeg_system.frameNStart = frameN  # exact frame index
        select_eeg_system.setAutoDraw(True)
    
    # *eeg_resp* updates
    if t >= 0.0 and eeg_resp.status == NOT_STARTED:
        # keep track of start time/frame for later
        eeg_resp.tStart = t  # underestimates by a little under one frame
        eeg_resp.frameNStart = frameN  # exact frame index
        eeg_resp.status = STARTED
        # keyboard checking is just starting
        eeg_resp.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if eeg_resp.status == STARTED:
        theseKeys = event.getKeys(keyList=['1', '2', '3', 'space', 'esc'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            eeg_resp.keys = theseKeys[-1]  # just the last key pressed
            eeg_resp.rt = eeg_resp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in do_triggersComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "do_triggers"-------
for thisComponent in do_triggersComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if eeg_resp.keys in ['', [], None]:  # No response was made
   eeg_resp.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('eeg_resp.keys',eeg_resp.keys)
if eeg_resp.keys != None:  # we had a response
    thisExp.addData('eeg_resp.rt', eeg_resp.rt)
thisExp.nextEntry()

# VERY exhaustive - can i do this better?
my_key_pressed = eeg_resp.keys
eeg_systems = {'1':'none', '2':'egi', '3':'bp'} # of course it is a comma - like everything in pyhton
eeg_system_used = eeg_systems[my_key_pressed]

print eeg_system_used
# the Routine "do_triggers" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "instr"-------
t = 0
instrClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
# instantiate_ev_thread
if eeg_system_used == 'none':
    evt = ev_thread(none_sender())
    

elif eeg_system_used == 'bp':
    evt = ev_thread(brain_products_sender())
    

elif eeg_system_used == 'egi':
    evt = ev_thread(egi_sender())
    

# start the evt loop!
evt.start()
print('event struct - initialized')
print(evt.isAlive())
# send stuff now - with evt.send(10), for example.
# send it either in the main loop - or in the audio, video and letter threads - i passed the object over there, too.
key_begin = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_begin.status = NOT_STARTED
# keep track of which components have finished
instrComponents = []
instrComponents.append(instr_text)
instrComponents.append(key_begin)
for thisComponent in instrComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instr"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instrClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # *instr_text* updates
    if t >= 0.0 and instr_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        instr_text.tStart = t  # underestimates by a little under one frame
        instr_text.frameNStart = frameN  # exact frame index
        instr_text.setAutoDraw(True)
    
    # *key_begin* updates
    if t >= 0.0 and key_begin.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_begin.tStart = t  # underestimates by a little under one frame
        key_begin.frameNStart = frameN  # exact frame index
        key_begin.status = STARTED
        # keyboard checking is just starting
        key_begin.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if key_begin.status == STARTED:
        theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_begin.keys = theseKeys[-1]  # just the last key pressed
            key_begin.rt = key_begin.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "instr"-------
for thisComponent in instrComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if key_begin.keys in ['', [], None]:  # No response was made
   key_begin.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('key_begin.keys',key_begin.keys)
if key_begin.keys != None:  # we had a response
    thisExp.addData('key_begin.rt', key_begin.rt)
thisExp.nextEntry()
# the Routine "instr" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "main_routine"-------
t = 0
main_routineClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
# instantiate_ev_thread
#if eeg_system_used == 'none':
#    evt = ev_thread(none_sender())
#    

#elif eeg_system_used == 'bp':
#    evt = ev_thread(brain_products_sender())
#    

#elif eeg_system_used == 'egi':
#    evt = ev_thread(egi_sender())
#    

# start the evt loop!
#evt.start()
#print('event struct - initialized')
#print(evt.isAlive())
# send stuff now - with evt.send(10), for example.
# send it either in the main loop - or in the audio, video and letter threads - i passed the object over there, too.
# DO ALL DECLRATIONS HERE
# this code block has 2 functions - (1) control time flow of the experimen, and (2) control visual elements/flashes

import time
checkerboard_hidden=True
# for future reference: I need a struct (!) telling me what is 'inside' the visual stimulus - at all times!!

# generated with a matlab script, so we can play around with other timing options
# stuff that happens left is always equally long as stuff that happens right - good for fMRI
# difference between 2 frequencies I cannot make exactly the same - so anything that compares frequencies should have NORMALIZED power

only_audio = [[10.,20.,'audio',['left','40']],[112.5,130.,'audio',['left','40']],[242.5,260.,'audio',['left','40']],[50.,60.,'audio',['left','55']],[195.,205.,'audio',['left','55']],[312.5,330.,'audio',['left','55']],[30.,40.,'audio',['right','40']],[147.5,165.,'audio',['right','40']],[277.5,295.,'audio',['right','40']],[77.5,95.,'audio',['right','55']],[175.,185.,'audio',['right','55']],[215.,225.,'audio',['right','55']]]
only_video = [[17.5,35.,'video',['left','8']],[135.,145.,'video',['left','8']],[280.,290.,'video',['left','8']],[87.5,105.,'video',['left','13']],[217.5,235.,'video',['left','13']],[320.,330.,'video',['left','13']],[52.5,70.,'video',['right','8']],[155.,165.,'video',['right','8']],[300.,310.,'video',['right','8']],[115.,125.,'video',['right','13']],[182.5,200.,'video',['right','13']],[252.5,270.,'video',['right','13']]]

# this lasts for 5 minutes and 40 seconds in total (last 10 secs is REST)
all_stims = [[10.,20.,'audio',['left','40']],[112.5,130.,'audio',['left','40']],[242.5,260.,'audio',['left','40']],[50.,60.,'audio',['left','55']],[195.,205.,'audio',['left','55']],[312.5,330.,'audio',['left','55']],[30.,40.,'audio',['right','40']],[147.5,165.,'audio',['right','40']],[277.5,295.,'audio',['right','40']],[77.5,95.,'audio',['right','55']],[175.,185.,'audio',['right','55']],[215.,225.,'audio',['right','55']],[17.5,35.,'video',['left','8']],[135.,145.,'video',['left','8']],[280.,290.,'video',['left','8']],[87.5,105.,'video',['left','13']],[217.5,235.,'video',['left','13']],[320.,330.,'video',['left','13']],[52.5,70.,'video',['right','8']],[155.,165.,'video',['right','8']],[300.,310.,'video',['right','8']],[115.,125.,'video',['right','13']],[182.5,200.,'video',['right','13']],[252.5,270.,'video',['right','13']]]
all_timings = all_stims
max_time = 340.;


# right checkerboard stimuli
right_cb = visual.RadialStim(win, tex='sqrXsqr', color=1, size=2.*SIZE_MUL_FACTOR,
                             visibleWedge=[0., 181.], radialCycles=5,
                             angularCycles=10, interpolate=False, 
                             angularPhase=2*3.141592/360/20,autoLog=False)
# right_cb_fl=right_cb
# right_cb_fl.setAngularPhase(90)
  
# left checkerboard stimuli
left_cb = visual.RadialStim(win, tex='sqrXsqr', color=1, size=2.*SIZE_MUL_FACTOR,
                            visibleWedge=[179.99, 360.], radialCycles=5,
                            angularCycles=10, interpolate=False,
                            angularPhase=2*3.141592/360/20,autoLog=False)
# left_cb_fl=left_cb
# left_cb_fl.setAngularPhase(90)

  
# fixation dot
fixation = visual.PatchStim(win, color=-0.25, colorSpace='rgb', tex=None,
                            mask='circle', size=0.12*SIZE_MUL_FACTOR)


vis_contents = [right_cb,left_cb,fixation,text_stim]


def doFlash(win,vis_contents,side,freq,evt,lstream_ev_container):

    # extract again the visual contents:
    right_cb = vis_contents[0]
    left_cb=vis_contents[1]
    fixation=vis_contents[2]
    text_stim=vis_contents[3]

    if side=='left':
        left_cb.contrast = -1.*left_cb.contrast
    elif side=='right':
        right_cb.contrast = -1.*right_cb.contrast
    left_cb.draw()
    right_cb.draw()
    fixation.draw()
    text_stim.draw()

    # when for text, only a flip will be done with the checkerboard - send it here!
    while len(lstream_ev_container)>0:
        evt.send(lstream_ev_container.pop(0))

    win.flip()

    # maybe skip this?
    if vis_do_double_flip:
        time.sleep(0.005)

        if side=='left':
            left_cb.contrast = -1.*left_cb.contrast
        elif side=='right':
            right_cb.contrast = -1.*right_cb.contrast
        left_cb.draw()
        right_cb.draw()
        fixation.draw()
        text_stim.draw()
        win.flip()


# seems to be a good thing to name it like this.
def hideCheckerboard(win,vis_contents,lstream_ev_container):

    right_cb = vis_contents[0]
    left_cb=vis_contents[1]
    fixation=vis_contents[2]
    text_stim=vis_contents[3]
    fixation.draw()
    text_stim.draw()

    # ugly code to make letters work nice with other flip() stuff that I do..
    while len(lstream_ev_container)>0:
        evt.send(lstream_ev_container.pop(0))
    

    win.flip()
    new_vis_contents = [fixation,text_stim]
    return new_vis_contents


def showCheckerboard(win,vis_contents):

    right_cb = vis_contents[0]
    left_cb=vis_contents[1]
    fixation=vis_contents[2]
    text_stim=vis_contents[3]
    left_cb.draw()
    right_cb.draw()
    fixation.draw()
    text_stim.draw()
    new_vis_contents = [right_cb,left_cb,fixation,text_stim]
    return new_vis_contents
    


def textFlip(win,vis_contents,video_is_running,lstream_ev_container):
    # well - this could use some improvements - in conceptualization.
    # the checkerboard_hidden could be done better.
    # that's what you get when you are programming quick -n- dirty.
   
    # if the checkerboard is doing stuff - then just let the checkerboard refresh also the letter.
    # in there, there's all the draw methods that u need!
    # otherwise - do it ourselves.
    # print video_is_running
    if video_is_running:
        pass
    else:
        # print(len(vis_contents))
        for item in vis_contents:
            item.draw()

        # ugly code to make letters work nice with other flip() stuff that I do.
        while len(lstream_ev_container)>0:
            print(lstream_ev_container)
            evt.send(lstream_ev_container.pop(0))
        win.flip()
        # empty it








# START MAIN EXPERIMENT HERE:
start_time=time.time()

# to control for showing(or not(!)) the checkerboard, to it like this:
video_is_running = 0
video_was_running = 0
audio_is_running = 0
audio_was_running = 0

# this is to make lstream events only be sent RIGHT before a window flip.
# I flip windows ONLY during checkerboard reversals, hide/show checkerboard - when VIS is ON
# when VIS is OFF, I flip windows separately.
# otherwise, I ask to flip the window TWICE during visual checkerboard stimulus - also with each letter - something I'd like to avoid, if possible.
#
#
# I need to read up on screen refresh rates and pyglet and pygame draw() and flip() methods.
#
lstream_ev_container=[]

# draw (only) the fixation cross, now, using the function:
new_vis_contents=hideCheckerboard(win,vis_contents,lstream_ev_container)

# control how/when audio and visual elements are created:
v_next = 0
a_next = 0


# just start a separate thread - that contain letters, and which switches the letter - in memory - once per second
# one the letter is changed - set a 'changed' flag appropriately (i.e., that I can query)
# inside this loop - just query this thread - ask it if it changed - if it did, update the letter (& 'flip' the window)
letter_switch_interval = 1.0 # seconds
letter_switch_probability = 0.33 # 15 % change of switching the 'wrong' way = subjects have to press.
# the letters list has been defined somewhere else (previously!)
lstream = letter_stream(letters_for_letter_stream,letter_switch_interval,letter_switch_probability,evt)
lstream.start()

# gather lstreams in here, and empty them upon a window flip

time_of_other_half_reset = 0.

while True:
    current_time=time.time() - start_time

    # prevent you from seeing the checkerboard like hell. Frequency = 0.4 Hz; a little less than once/2 sec.
    if vis_flip_other_side and video_is_running:
        time_since_last_other_half_reset = current_time - time_of_other_half_reset

        if time_since_last_other_half_reset > vis_flip_other_side_interval:

            # duh.
            time_of_other_half_reset = current_time

            # if you have video_is_running, you definitely have a v_current that's an object.
            side = v_current.getSide()
            # print side
            # print(time_since_last_other_half_reset)
            # print(time_of_other_half_reset)

            if side == 'left':
                right_cb.contrast = -1.*right_cb.contrast
            elif side == 'right':
                left_cb.contrast = -1.*left_cb.contrast

        else:
            pass

    # check out what we should do right now.
    tasks=[]
    for item in all_timings:
        if current_time > item[0] and current_time < item[1]:
            tasks.append([item[2], item[3]])
    
    # keep track of them over here (!) - so thay they are (properly!!!) reset!
    video_is_running = 0
    audio_is_running = 0


    for task in tasks:
    
        action = task[0]
        options = task[1]
    
        # set the is_now_running to: zero - so that at the end of this loop, the is_now_running == 1 whenever a checkerboard vis_stim is present.

        if action=='video':

           # only set this to 1 if there is a task - 'video' in the task stack.
            video_is_running = 1

            # only set the checkerboard to true if it was off, first.
            if not video_was_running:
                print(' -- ENABLE CHECKERBOARD')
                new_vis_contents = showCheckerboard(win,vis_contents)


            # only create the v_next, if its value is not the (int) 0 value - so do THIS at first iteration of the block.
            # so - at the start; make an thread - and start it - and make a new thread just after that, just in case
            if v_next==0:
                v_current = play_vis_stim(vis_times,options[0],options[1],evt)
                v_current.start()
                v_next = play_vis_stim(vis_times,options[0],options[1],evt)
            else:
                # when NOT at the start - cycle to the next one - start it - prepare the new one already.
                # only start up the visual new thread once the current one is done (IF the task has a video element in it)
                if not v_current.isAlive():     
                    v_current=v_next
                    v_current.start()
                    v_next = play_vis_stim(vis_times,options[0],options[1],evt)


        # handle the 'audio:
        if action=='audio':

            # mark audio is running(now)
            audio_is_running = 1


            # same handling for audio.
            if a_next==0:
                a_current=play_audio_stim(sounds,options[0],options[1],evt)
                a_current.start()
                a_next=play_audio_stim(sounds,options[0],options[1],evt)
            else:
                if not a_current.isAlive():                
                    a_current = a_next
                    a_current.start()
                    # send a trig! - let the audio do it, itself - no need to clog my code here.
                    a_next=play_audio_stim(sounds,options[0],options[1],evt)
                    


    # break the main loop if time is over:
    if current_time > max_time:
        # a graceful exit for the thread which normally wouldn't end...
        lstream.setStop()
        break



    # do the check here for either showing, or hiding, the checkerboards. Probably I can also ask for which elements are in the current visual stimulus.
    # need pygame manual for that...
    if video_was_running and not video_is_running:
        print(' -- DISABLE CHECKERBOARD')
        new_vis_contents = hideCheckerboard(win,vis_contents,lstream_ev_container)

    
    # reset the video and/or audio stimuli:
    if not video_is_running:
        v_next = 0
    if not audio_is_running:
        a_next = 0


    # check if the visual thread is running, if so:
    # sort of assumes that there are checkerboard!
    if video_is_running:
        if v_current.queryFlash():
            # do the flash
            side = v_current.getSide()
            freq = v_current.getFreq()
            # send a code indicating a flash to my evt handler object thread - fire & forget..?
            evt.send(visual_evt_codes[side][freq])
            doFlash(win,vis_contents,side,freq,evt,lstream_ev_container)

            # reset the flash value - and continue:
            v_current.resetFlash()




    # and now - handle the beginning and endings of audio and visual; according to the example above.
    # long-winded code block to resolve events:
    # what's happening should be straightforward.
    if video_was_running and not video_is_running:
        # send a video end marker
        freq = v_current.getFreq()
        side = v_current.getSide()
        evt.send(visual_evt_codes_end[side][freq])

    if video_is_running and not video_was_running:
        # send a video begin marker
        freq = v_current.getFreq()
        side = v_current.getSide()
        evt.send(visual_evt_codes_begin[side][freq])

    if audio_was_running and not audio_is_running:
        # send an audio end marker
        freq = a_current.getFreq()
        side = a_current.getSide()
        evt.send(audio_evt_codes_end[side][freq])

    if audio_is_running and not audio_was_running:
        # send an audio begin marker
        freq = a_current.getFreq()
        side = a_current.getSide()
        evt.send(audio_evt_codes_begin[side][freq])


   # to keep track, do it like this:
    video_was_running = video_is_running
    audio_was_running = audio_is_running

    time.sleep(0.0005) # be kind to the computer - we won't need crazy timing accuracy - just accurate markers.



    # resolve letter stream.
    if lstream.queryFlag():
        letter = lstream.getLetter()
        ltype = lstream.getType()

        # send my letter event!!
        # print('trying to send: ' + str(txt_evt_codes[ltype]))
        evt.send(txt_evt_codes[ltype])
        lstream_ev_container.append(txt_evt_codes[ltype]+10)
        # stream_ev_container=[]

        text_stim.text=letter
        text_stim.text=text_stim.text # according to suggestion??
        textFlip(win,new_vis_contents,video_is_running,lstream_ev_container)
        

    # ADD-ON which only works in psychopy?
    # enable key break...
    # do the key
    if event.getKeys(keyList=["escape"]):
        # stop my letter stream:
        lstream.setStop()
        # stop my event handler:
        evt.stop()
        core.quit()
        continueRoutine=False

#    key = event.getKeys() # \also check for a keyboard trigger (any key) 
#    if len(key) > 0:
#       if not key == ['space']:
#          pass
#     else:
#         if key == ['escape']: core.quit() #  escape allows us to exit
#        continueRoutine = False


# keep track of which components have finished
main_routineComponents = []
for thisComponent in main_routineComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "main_routine"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = main_routineClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in main_routineComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "main_routine"-------
for thisComponent in main_routineComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


# the Routine "main_routine" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "end"-------
t = 0
endClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
end_key = event.BuilderKeyResponse()  # create an object of type KeyResponse
end_key.status = NOT_STARTED

# keep track of which components have finished
endComponents = []
endComponents.append(end_text)
endComponents.append(end_key)
for thisComponent in endComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "end"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = endClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_text* updates
    if t >= 0.0 and end_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        end_text.tStart = t  # underestimates by a little under one frame
        end_text.frameNStart = frameN  # exact frame index
        end_text.setAutoDraw(True)
    
    # *end_key* updates
    if t >= 0.0 and end_key.status == NOT_STARTED:
        # keep track of start time/frame for later
        end_key.tStart = t  # underestimates by a little under one frame
        end_key.frameNStart = frameN  # exact frame index
        end_key.status = STARTED
        # keyboard checking is just starting
        end_key.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if end_key.status == STARTED:
        theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            end_key.keys = theseKeys[-1]  # just the last key pressed
            end_key.rt = end_key.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if end_key.keys in ['', [], None]:  # No response was made
   end_key.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('end_key.keys',end_key.keys)
if end_key.keys != None:  # we had a response
    thisExp.addData('end_key.rt', end_key.rt)
thisExp.nextEntry()
# stop my letter stream:
# stop my event handler:
evt.stop()
core.quit()
continueRoutine=False


# the Routine "end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()







# aand... stop the evt's - at the end of the experiment.
# should be fine.. I hope.
evt.stop()

lstream.setStop()

win.close()
core.quit()
