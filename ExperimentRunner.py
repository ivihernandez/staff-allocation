'''
Created on Sep 29, 2012

@author: ivihernandez
'''
#standard imports

#non standard imports
import inspyred
import random
import sys
#ivan's imports
sys.path.append('../myutils')
import myutils
import SimulatorRunner
import nsga2
import psda
import StaffAllocationProblem

class ExperimentRunner:
    def __init__(self, seeds, parameterReader):
        self.archiver = inspyred.ec.archivers.best_archiver
        self.seeds = seeds
        
        self.prng = random.Random()
        self.prng.seed(seeds[0])
        self.parameterReader = parameterReader
    def run(self, runs, population, generations):
        solutions = []#store several solutions
        totalPopulation = []#store the population for the final pareto
        myArchive = []#store the pareto of the several runs
        problem = StaffAllocationProblem.StaffAllocationProblem(seeds=self.seeds,
                                                                parameterReader=self.parameterReader)
        for i in xrange(1, runs + 1):
            print "Experiment Runner", i
            sol = nsga2.nsga2_integer(prng=self.prng,
                                      popSize=population,
                                      generations=generations,
                                      problem=problem,
                                      seeds=[])
            solutions.append(sol)
            for ind in sol.archive:
                totalPopulation.append(ind)
    
        self.myArchive = self.archiver(random=self.prng,
                             population=list(totalPopulation),
                             archive=list(myArchive),
                             args=None)
        for sol in myArchive:
            print sol
        
        
        
        #final_arc = myArchive
        
        """
        import pylab
        x = []
        y = []
        for f in final_arc:
            y.append(f.fitness[0])
            x.append(f.fitness[1])
        pylab.scatter(x, y, color='b')
        pylab.ylabel("Avg. Waiting Time")
        pylab.xlabel("Total staff")
        pylab.savefig('%s Example (%s).pdf' % ("nsga2", problem.__class__.__name__), format='pdf')
        if doPlot:
            pass#pylab.show()
        """
    def get_pareto(self):
        """
            @postcondition: the function run from this class should have been called.
        """
        return self.myArchive