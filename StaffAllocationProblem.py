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
import myutils
class StaffAllocationProblem():
    def __init__(self, seeds, parameterReader):
        self.maximize = True
        #minimize Waiting time, minimize Resources, maximize throughput  
        #minimize resources, maximize throughput
        self.objectiveTypes = [False, True]
        self.dimensions = 4 # greeter, screener, dispenser, medic
        #self.maxEmployeesPerStation = 45
        
        
        #parameters (e.g. preScreenedPercentage)
        self.parameterReader = parameterReader
        
        
        # greeter, screener, dispenser, medic
        self.lowerBounds = [1, 1, 1, 1]
        self.upperBounds = [45, 45, 45, 5] 
        #self.lowerBounds = [1, 1, 1, 1]
        #self.upperBounds = [3, 3, 3, 3]
        
        #self.bounder = inspyred.ec.Bounder(1, 4)
        self.bounder = inspyred.ec.Bounder(self.lowerBounds, self.upperBounds)
        self.seeds = seeds
        self.boundingParameters = {}
        self.boundingParameters['lowerBounds'] = self.lowerBounds
        self.boundingParameters['upperBounds'] = self.upperBounds
    
    def evaluator(self, candidates, args):
        
        fitness = []
        for capacities in candidates:
            #capacities = myutils.boundingFunction(capacities, self.boundingParameters)
            scores = []
            simulatorRunner = SimulatorRunner.SimulatorRunner()
            
            simulatorRunner.run(seeds=self.seeds,
                                capacities=capacities,
                                parameterReader=self.parameterReader)
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
        
        greeters = random.randint(self.lowerBounds[0], self.upperBounds[0])
        screeners = random.randint(self.lowerBounds[1], self.upperBounds[1])
        dispensers = random.randint(self.lowerBounds[2], self.upperBounds[2])
        medics = random.randint(self.lowerBounds[3], self.upperBounds[3])
        choices = [greeters, screeners, dispensers, medics]
        print 'choices', choices
        return choices
        """
        choices = range(1, self.maxEmployeesPerStation)
        retval = [random.choice(choices) for _ in xrange(self.dimensions )]
        return retval
        """