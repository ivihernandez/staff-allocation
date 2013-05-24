'''
Created on Sep 23, 2012

@author: ivihernandez
'''
#standard imports
import datetime
from os import listdir
from os.path import isfile, join
import os, inspect, sys

#non standard imports

#ivan's imports
import ParameterReader
#import SimulatorRunner
import SolutionWriter
import ExperimentRunner

def load_modules_manually():
    """
        This function lets me use my other scripts.
        It is necessary if running the program outside Aptana.
        Aptana knows where the other modules are, thanks to the
        external references properties.
    """
    #cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
    cmd_folder = '../myutils/'
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)
    #print sys.path
def main():
    load_modules_manually()
    #sys.exit()
    mypath = r'./experiments-to-run'
    experimentFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
    seeds = [123, 456, 789]
    
    for experimentFile in experimentFiles:
        parameterReader = ParameterReader.ParameterReader(join(mypath,experimentFile))
        experimentRunner = ExperimentRunner.ExperimentRunner(seeds, parameterReader)
        experimentRunner.run(runs=1,
                             population=100,
                             generations=20)
        solutionWriter = SolutionWriter.SolutionWriter(join(mypath,experimentFile),experimentRunner)
        solutionWriter.dumpSolution()
    
    
        
if __name__ == '__main__':
    startTime = datetime.datetime.now()
    print 'program started', startTime
    main()
    endTime = datetime.datetime.now()
    print 'program finished',endTime 
    print 'simulation lenght =', endTime - startTime