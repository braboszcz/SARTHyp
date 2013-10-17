'''
Script for Sustained Attention To Response Task combined with Thought Probes

'''
from psychopy import visual, event, core, data, logging, gui
import time
import os, sys

 

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
# Setup files for logfile  saving
#---------------------------------------

if not os.path.isdir('Logdata'):
	os.makedirs('Logdata')  # if this fails (e.g. permissions) we will get error
        filename = 'Logdata' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
        logging.setDefaultClock(globalClock)
        logFileExp = logging.LogFile(filename +'.log', level=logging.EXP)
        logging.console.setLevel(logging.INFO)  # this outputs to the screen, not a file


#---------------------------------------
# Create timers
#---------------------------------------
globalClock = core.Clock()  # to track the time since experiment started
respTime = core.Clock()
trialClock = core.Clock()

