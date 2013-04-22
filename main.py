'''
Created on Sep 23, 2012

@author: ivihernandez
'''
#standard imports
import datetime

#non standard imports

#ivan's imports
#import SimulatorRunner
import ExperimentRunner
"""
def main():
    nsimul = 1
    seed = 2313
    #greeter, screener, dispenser, medic]
    capacities = [1,2,3,1]
    simulatorRunner = SimulatorRunner.SimulatorRunner()
    simulatorRunner.run(nsimul=nsimul,
                        seed=seed,
                        capacities=capacities)
""" 
def main():
    seeds = [123, 456, 789]
    experimentRunner = ExperimentRunner.ExperimentRunner(seeds)
    experimentRunner.run(runs=1,
                         population=100,
                         generations=20)
    
    
        
if __name__ == '__main__':
    startTime = datetime.datetime.now()
    print 'program started', startTime
    main()
    endTime = datetime.datetime.now()
    print 'program finished',endTime 
    print 'simulation lenght =', endTime - startTime