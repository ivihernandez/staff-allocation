'''
Created on Sep 23, 2012

@author: ivihernandez
'''
#standard imports
import datetime
from os import listdir
from os.path import isfile, join
#non standard imports

#ivan's imports
import ParameterReader
#import SimulatorRunner
import SolutionWriter
import ExperimentRunner

def main():
    
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