'''
Generate trias list for SART task: 1 to 9 numbers with number 3 10% rare target and thought probe
Occurrences of targets and thought probes events are pseudorandomized and uniformely distributed within sessions so 
that there is between 5 to 15 trials between each event and each distance has the same number of occurences
'''

import random 
import csv
import os
import numpy


GO = 1
NOGO = 2
PROBE = 3

Trig_go = int("10010000",2)
Trig_nogo = int("01001000",2)
Trig_probe = int("00100100",2)
Trig_break = int("00010010",2)

def genSARTList(numStimPerBlock, numBlock):
	writeTrials = csv.writer(open('mytrialList.csv','wb'), delimiter = ',', quotechar = '"')
        header = ['stim', 'condition', 'block', 'response', 'response time', 'stim onset', 'trigger']
        writeTrials.writerow(header)


	#------------------------------------------------------------------------
        # define numbers of each type of trials
        #------------------------------------------------------------------------
        nGo = numStimPerBlock*90/100
        nNoGo = numStimPerBlock*5/100
	nProbe = numStimPerBlock*5/100
	

	
	
	#------------------------------------------------------------------------
        # create trial list for each  block
        #------------------------------------------------------------------------
					
	def def_trials():
		trials = [GO]*nGo
		# get target indices
		ind_target = range(5,16)*((nNoGo+nProbe)/len(range(5,15)))
		random.shuffle(ind_target)
		# create list of targets
		target_list = [PROBE]*nProbe
		target_list += [NOGO]*nNoGo
		random.shuffle(target_list)

		next_target = 0
		for i in range(len(target_list)):
			next_target += ind_target[i]
			target = target_list.pop()
			trials.insert(next_target,target )
		return trials

	pause = []
	for j in range(numBlock):
		trials = []
		trials = def_trials()
		go_list = ['1','2','4','5','6','7','8','9']#*nGo
		random.shuffle(go_list)
		trial = []
		last_stim = 0
		for n in range(len(trials)):
			if trials[n] == 2:	
				trial = ['3','nogo', j+1,'','','', Trig_nogo]
			elif trials[n] == 3:
				trial = ['probe','probe', j+1,'','','', Trig_probe]
			else: 
				stim = random.choice(go_list)
				while stim == last_stim:
					stim = random.choice(go_list)
				trial = [stim, 'go', j+1,'','','', Trig_go]
				last_stim = stim
			writeTrials.writerow(trial)
			print trial
		if j+1 ==  numBlock:
			end = ['end', 'end', j+1,'','','', Trig_break ]
			writeTrials.writerow(end)
		else:
			pause = ['break', 'break', j+1,'','','', Trig_break]
			writeTrials.writerow(pause)

	


genSARTList(300,2)		
