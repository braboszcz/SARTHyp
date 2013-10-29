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
globalClock = core.Clock()  # to track the time since experiment started
respTime = core.Clock()
trialClock = core.Clock()

#---------------------------------------
# Setup files for logfile  saving
#---------------------------------------

if not os.path.isdir('Logdata'):
	os.makedirs('Logdata')  # if this fails (e.g. permissions) we will get error
filename = 'Logdata' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logging.setDefaultClock(globalClock)
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
pos=[0, 0], height=0.06,
color='black')
fixation.setLineWidth = 0.4


#---------------------------------------
# instructions
#---------------------------------------
instruct = visual.TextStim(win = win, ori = 0, name = 'instruct', 
	text = 'Presser le bouton lorsqu''un chiffre apparait SAUF pour le 3 \n\n Appuyez sur espace pour continuer ',
	 pos=[0, 0], height=0.04, wrapWidth=None,
         color='white', colorSpace='rgb', opacity=1.0,
         depth=0.0)

pause = visual.TextStim(win = win, ori = 0, name = 'pause', 
	text = 'Pause \n\n Appuyez sur espace pour continuer ',
	 pos=[0, 0], height=0.04, wrapWidth=None,
         color='white', colorSpace='rgb', opacity=1.0,
         depth=0.0)
probe = 


#--------------------------------------
# Start Experiment
#--------------------------------------
win.setRecordFrameIntervals(True) # frame time tracking
globalClock.reset()


#--------------------------------------
# Show Instructions
#--------------------------------------
instruct.draw(win)
win.flip()
event.waitKeys(keyList= 'space')


#--------------------------------------
# Run TAsk
#--------------------------------------

for thisTrial in trials:
	trials.saveAsWideText(filename + '.csv', delim = ';', appendFile = False)
	
	thisRespKey = []
	
	
	if thisTrial['Condition'] != 'break' and thisTrial['Condition'] != 'probe':
		stim = visual.TextStim(win, text = thisTrial['Stim'])
		stim.draw()
		win.flip() 
		core.wait(ISI)
	
	elif thisTrial['Condition'] == 'break':
		pause.draw(win)
		win.flip()
		event.waitKeys(keyList = 'space')
	
	else:
		

	if event.getKeys(['q', 'escape']):
		win.close()
		core.quit()


