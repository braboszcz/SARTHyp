# -*- coding: utf8 -*-
#!/usr/bin/env python
'''
Script for Sustained Attention To Response Task combined with Thought Probes

'''

from psychopy import visual, event, core, data, logging, gui
import time
import os, sys


#---------------------------------------
# Set Variables
#---------------------------------------

TRIALS_FILE = 'trialList.csv'
ISI = 1.5

 

#---------------------------------------
# Store info about the experiment session
#---------------------------------------

expName = 'SARTHyp'
expInfo = {'participant':'', 'gender (m/f)':'', 'age':'', 'session':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel  
expInfo['date'] = data.getDateStr()  # add a simple timestamp  
expInfo['expName'] = expName

# Experiment handler
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=False, saveWideText=False) #prevent the experiment handler to write expe data upon termination (and overwriting our files)

#---------------------------------------
# Load trial files 
#---------------------------------------

# read from csv file
trialList = data.importConditions(TRIALS_FILE, returnFieldNames=False)
trials = data.TrialHandler(trialList, nReps=1, method='sequential', extraInfo=expInfo)
trials.data.addDataType('respKey')
trials.data.addDataType('respTime')
trials.data.addDataType('stimOnset')

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
filename = 'Logdata' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logging.setDefaultClock(trialClock)
logFileExp = logging.LogFile(filename +'.log', level=logging.EXP)
logging.console.setLevel(logging.DEBUG)  # this outputs to the screen, not a file



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

for thisTrial in trials:
	trials.saveAsWideText(filename + '.csv', delim = ';', appendFile = False)
	
	thisRespKey = []
	RespKey = []
	stimOnset = trialClock.getTime()
	
	if thisTrial['Condition'] == 'break':
		fin_block = visual.TextStim(win = win, ori = 0, text = u"Bloc numéro %s terminé.\n Vous pouvez faire une pause \n Appuyer sur 'entrée' pour continuer " %thisTrial['Block'],
	alignHoriz = 'center', alignVert='center', height=0.04, color='white')
		fin_block.draw()
	
	elif thisTrial['Condition'] == 'breakHypno':
		fin_block = visual.TextStim(win = win, ori = 0, text = u"Bloc numéro %s terminé. L'expérience va continuer" %thisTrial['Block'],
alignHoriz = 'center', alignVert='center', height=0.04, color='white')
		fin_block.draw()

		
		win.flip()
		thisRespKey = event.waitKeys(keyList = 'return')
		fixation.draw()
		win.flip()
		core.wait(2)
	
	elif thisTrial['Condition'] == 'probe':
		probe_signe.draw(win)
		win.flip()
		core.wait(0.5)
		probe.draw(win)
		win.flip()
		thisRespKey = event.waitKeys(keyList = ['1', '2', '3', '4'])
		fixation.draw()
		win.flip()
		core.wait(2)	
	
	else:
		stim = visual.TextStim(win, text = thisTrial['Stim'], height = 0.1)
		stim.draw()
		win.flip() 
		thisRespKey = event.getKeys()
		core.wait(ISI)


	if len(thisRespKey)>0 : # at least one key was pressed
		RespKey = thisRespKey[-1] # get just the last key pressed
		ResponseTime = trialClock.getTime()
	
	#--------------------------------------
	# store trial data
	#--------------------------------------
	
	trials.addData('stimOnset', stimOnset)
	if RespKey != []:
		trials.addData('respKey',RespKey)
		trials.addData('respTime', ResponseTime)
	thisExp.nextEntry()
			

	if event.getKeys(['q', 'escape']):
		win.close()
		core.quit()

the_end.draw()
win.flip()
core.wait(5)
totaltime = expeClock.getTime()/60
print totaltime

win.close()
core.quit()


