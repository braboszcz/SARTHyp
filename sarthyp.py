# -*- coding: utf8 -*-
#!/usr/bin/env python
'''
Script for Sustained Attention To Response Task combined with Thought Probes

'''

from psychopy import visual, event, core, data, logging, gui
import time
import os, sys
from psychopy import parallel
#import myparport as mp

from ppc import csvWriter

#---------------------------------------
# Set Variables
#---------------------------------------

TRIALS_FILE = 'mytrialList.csv' #trialList_Hypno.csv ; trialList_Normal.csv # reads the trial list file
ISI = 1.5 # inter stim interval
validResponses = ['space', 'none']

parallel.setPortAddress(0x378) #888

#---------------------------------------
# Store info about the experiment session
#---------------------------------------

expName = 'SARTHyp'
expInfo = {'participant':'', 'session':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel  
expInfo['date'] = data.getDateStr()  # add a simple timestamp  


# Experiment handlerr
#thisExp = data.ExperimentHandler(name=expName, version='',
#    extraInfo=expInfo, runtimeInfo=None,
#    originPath=None,
#    savePickle=False, saveWideText=False) #prevent the experiment handler to write expe data upon termination (and overwriting our files)

#----------------------------------
# Load trial files 
#---------------------------------------

# read from csv file
trialList = data.importConditions(TRIALS_FILE, returnFieldNames=False)
#trials = data.TrialHandler(trialList, nReps=1, method='sequential') #, extraInfo=expInfo
#trials.data.addDataType('respKey')
#trials.data.addDataType('respTime')
#trials.data.addDataType('stimOnset')

#---------------------------------------
# Create timers
#---------------------------------------
trialClock = core.Clock() 
expeClock = core.Clock()  # to track the time since experiment started

#---------------------------------------
# Setup files for logfile  saving
#---------------------------------------

if not os.path.isdir('Logdata'):
	os.makedirs('Logdata')  # if this fails (e.g. permissions) we will get error
filename = 'Logdata' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['session'])
logging.setDefaultClock(trialClock)
logFileExp = logging.LogFile(filename +'.log', level=logging.EXP)
logging.console.setLevel(logging.DEBUG)  # this outputs to the screen, not a file

writer = ppc.csvWriter(expInfo['participant'] + '_' + expInfo['session'], 'data')

#---------------------------------------
# Setup Window
#---------------------------------------

win = visual.Window((1280,1024), color=[0,0,0], monitor = 'testMonitor', 
units = 'height', fullscr = False, colorSpace = 'rgb')  


#---------------------------------------
# Hypnosis  Induction Routine
#---------------------------------------
def induction():
	fixation.draw()
        win.flip()
	even.waitKeys(KeyList = 'space')


#---------------------------------------
# Fixation cross
#---------------------------------------


fixation=visual.TextStim(win=win, ori=0, name='fixation_cross',
text='+',
font='Arial',
pos=[0, 0], height=0.1,
color='white')
fixation.setLineWidth = 0.4


#---------------------------------------
# instructions
#---------------------------------------
instruct = visual.TextStim(win = win, ori = 0, name = 'instruct', 
	text = u'''Appuyer sur 'espace' lorsqu'un chiffre apparait \n SAUF si c'est un 3 \n\n Appuyer sur 'entrée' pour continuer''',
	 pos=[0, 0], height=0.04, wrapWidth=None,
         color='white', colorSpace='rgb', opacity=1.0,
         depth=0.0)

the_end = visual.TextStim(win = win, ori = 0, 
	text = u"L'expérience est terminée ! " ,
	 alignHoriz = 'center', alignVert='center', height=0.04, wrapWidth=None,
         color='white', colorSpace='rgb', opacity=1.0,
         depth=0.0)

probe = visual.TextStim(win =  win, ori = 0, name = 'probe',
 text = u'''Quelle était votre expérience consciente juste avant l'apparition de cette question ? \n\n\n 1. Concentration sur l' exécution de la tâche (presser 1)\n\n 2. Pensées en lien avec la tâche mais ne concernant pas son exécution (presser 2) \n\n 3. Distraction provoquée par un bruit, une sensation (presser 3) \n\n 4.  Dérive attentionelle (presser 4)''', 
pos = [0,0], height = 0.03, color = 'white')

probe_signe = visual.TextStim(win=win, ori =0, name ='probe_signe', text = '?', pos = [0,0], height = 0.1, color = 'white')

#-------------------------------
# Function to get responses
#-------------------------------
def getKeyboardResponse(validResponses,duration= 0):
	"""Returns keypress and RT. Specify a duration (in secs) if you want response collection to last 
        that long. Unlike event.waitkeys(maxWait=..), this function will not exit until duration. 
        Use waitKeys with a maxWait parameter if you want to have a response deadline, but exit as soon 
        as a response is received."""
	event.clearEvents() #important - prevents buffer overruns
	responded = False
	timeElapsed = False
	rt = '*'
	responseTimer = core.Clock()
 
	if duration==0:
		responded = event.waitKeys(keyList=validResponses)
		rt = responseTimer.getTime()
		return [responded[0],rt] #only get the first response. no timer for waitKeys, so do it manually w/ a clock
	else:
		while responseTimer.getTime() < duration:
			if not responded:
				responded = event.getKeys(keyList=validResponses,timeStamped=responseTimer)
		if not responded:
			return [' ',' ']
		else:
			return responded[0]  #only get the first resp

def whatresp(respKey):
    code = None
    if respKey is '1':
        code = 111
    elif respKey is '2':
        code = 112
    elif respKey is '3':
        code = 113
    elif respKey is '4':
        code = 114
    elif respKey is 'space':
        code = 115

    return(code)


trigger_fixation = 0x0160
#--------------------------------------
# Start Experiment
#--------------------------------------
win.setRecordFrameIntervals(True) # frame time tracking
trialClock.reset()


#--------------------------------------
# Show Instructions
#--------------------------------------
instruct.draw(win)
win.flip()
event.waitKeys(keyList= 'return')
fixation.draw()
win.flip()
core.wait(2)

#--------------------------------------
# Run TAsk
#--------------------------------------

for thisTrial in trialList: #trials
    # trials.saveAsWideText(filename + '.csv', delim = ';', appendFile = False)
	
    parallel.setData(0) # sets all pin low
#	thisRespKey = []
    RespKey = []
    ProbeKey = []
    thisProbeKey = []
    stimOnset = trialClock.getTime()

    if thisTrial['condition'] == 'break':
        fin_block = visual.TextStim(win = win, ori = 0, text = u"Bloc numéro %s terminé.\n Vous pouvez faire une pause \n Appuyer sur 'entrée' pour continuer " %thisTrial['Block'], alignHoriz = 'center', alignVert='center', height=0.04, color='white')
        fin_block.draw()
        win.flip()
        parallel.setData(thisTrial['trigger'])
        core.wait(0.005)
        parallel.setData(0)

        thisRespKey = event.waitKeys(keyList = 'return')
        fixation.draw()
        win.flip()
        parallel.setData(trigger_fixation)
        core.wait(0.005)
        parallel.setData(0)
        core.wait(2)	
	
    elif thisTrial['condition'] == 'breakHypno':
        hypno = visual.TextStim(win = win, ori = 0, text = u"Bloc numéro %s terminé. L'expérience va continuer" %thisTrial['Block'],
alignHoriz = 'center', alignVert='center', height=0.04, color='white')
        hypno.draw()
        win.flip()
        parallel.setData(thisTrial['trigger'])
        core.wait(0.005)
        parallel.setData(0)
        fixation.draw()
        win.flip()
        parallel.setData(trigger_fixation)
        core.wait(0.005)
        parallel.setData(0)
        core.wait(2)
		
	
	
    elif thisTrial['condition'] == 'probe':
        probe_signe.draw(win)
        win.flip()
        parallel.setData(int(thisTrial['trigger']))
        core.wait(0.005)
        parallel.setData(0)
        core.wait(0.5)
        probe.draw(win)
        win.flip()
        thisProbeKey = getKeyboardResponse( ['1', '2', '3', '4'], duration = 0)
        Trig_probe = whatresp(thisProbeKey[0])
        if Trig_probe:
            parallel.setData(Trig_probe)
            core.wait(0.005)
            parallel.setData(0)
           

        fixation.draw()
        win.flip()
        parallel.setData(trigger_fixation)
        core.wait(0.005)
        parallel.setData(0)
        core.wait(2)	

    elif thisTrial['condition'] == 'end':
        the_end.draw()
        win.flip()
        core.wait(5)

    else:
        stim = visual.TextStim(win, text = thisTrial['stim'], height = 0.1)
        stim.draw()
        win.flip()
        parallel.setData(int(thisTrial['trigger']))
        core.wait(0.005)
        parallel.setData(0)

        #thisRespKey = event.waitKeys(maxWait= ISI, keyList = ['space', 'none'])
		#core.wait(ISI)
        thisRespKey = getKeyboardResponse('space', duration = ISI)
        Trig_resp = whatresp(thisRespKey[0])

        if Trig_resp:
            parallel.setData(Trig_resp)
            core.wait(0.005)
            parallel.setData(0)
            pass

	if len(thisRespKey)>0 : # at least one key was pressed
		RespKey = thisRespKey[0] # get keypress
		ResponseTime = thisRespKey[1] #get response time
        
	
	#--------------------------------------
	# store trial data
	#--------------------------------------
	
	thisTrial['stim onset'] =  stimOnset
	if RespKey != []:
		thisTrial['response'] =  RespKey
		thisTrial['response time'] =  ResponseTime
	if thisProbeKey != []:
		thistrial['response']= thisProbeKey       
		thistrial['response time'] = ResponseTime 		
#	thisExp.nextEntry()
	
	if event.getKeys(['q', 'escape']):
		win.close()
		core.quit()
    
    parallel.setData(0) # sets all pin low

totaltime = expeClock.getTime()/60
print totaltime

win.close()
core.quit()

