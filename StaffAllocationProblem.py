'''
Created on Sep 29, 2012

@author: ivihernandez
'''
#standard imports
import random
#non standard imports
import inspyred

#ivan's imports
import SimulatorRunner

class StaffAllocationProblem():
    def __init__(self, seeds):
        self.maximize = True
        #minimize Waiting time, minimize Resouces, maximize throughput  
        #minimize resources, maximize throughput
        self.objectiveTypes = [False, True]
        self.dimensions = 4 # greeter, screener, dispenser, medic
        self.maxEmployeesPerStation = 30
        self.bounder = inspyred.ec.Bounder(1, self.maxEmployeesPerStation)
        
        self.seeds = seeds
    def evaluator(self, candidates, args):
        
        fitness = []
        for capacities in candidates:
            scores = []
            simulatorRunner = SimulatorRunner.SimulatorRunner()
            
            simulatorRunner.run(seeds=self.seeds,
                                capacities=capacities)
            time = simulatorRunner.get_avg_waiting_times()
            resources = simulatorRunner.get_resource_count()
            throughput = simulatorRunner.get_processed_count()
            
            scores.append(resources)
            scores.append(throughput)
            scores.append(time)
            
            pareto = inspyred.ec.emo.Pareto(scores, self.objectiveTypes)
            fitness.append(pareto)
        
        return fitness
    def generator(self, random, args):
        choices = range(1, self.maxEmployeesPerStation)
        retval = [random.choice(choices) for _ in xrange(self.dimensions )]
        return retval