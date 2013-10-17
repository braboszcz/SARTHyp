'''
Generate trial list for SART task: 1 to 9 numbers with number 3 20% rare target and thought probe
Occurrences of targets and thought probes are pseudorandomized and uniformely distributed within sessions

'''

import random
import csv
import os
import numpy


GO = 1
NOGO = 2
PROBE = 3

def genSARTList(numStimPerBlock, numBlock):
	writeTrials = csv.writer(open('mytrialList.csv','wb'), delimiter = ',', quotechar = '"')
        header = ['Stim', 'Condition']
        writeTrials.writerow(header)



