'''
Created on Sep 29, 2012

@author: ivihernandez
'''
#standard imports

#non standard imports

#ivan's imports
import PODSimulation
import ResultsAnalyzer

class SimulatorRunner:
    def run(self, seeds, capacities):
        """
            @param seed: seed for random numbers
            @param nsimul: number of simulations per each capacity configuration
            @param capacities: array representing the number of resources per service   
        """
        #self.totalResources = sum(capacities) just to ensure
        self.avgWaitingTime = 0
        self.avgProcessedCount = 0
        self.totalResourceCount = 0
        simulations = []
        for seed in seeds:
            #greeter, screener, dispenser, medic]
            simul = PODSimulation.PODSimulation(capacities)
            simul.model(seed)
            simulations.append(simul)
            
        resultsAnalyzer = ResultsAnalyzer.ResultsAnalyzer(simulations)    
        
        self.avgWaitingTime = resultsAnalyzer.get_avg_total_waiting_time()
        self.avgProcessedCount = resultsAnalyzer.get_avg_total_number_out()
        self.totalResourceCount = resultsAnalyzer.get_total_resources()
        
        
        #simul.plot_stats()
    def get_processed_count(self):
        return self.avgProcessedCount
    def get_resource_count(self):
        return self.totalResourceCount
    def get_avg_waiting_times(self):
        return self.avgWaitingTime