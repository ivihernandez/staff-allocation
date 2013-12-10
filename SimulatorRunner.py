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
    def run(self, seeds, capacities, parameterReader):
        """
            @param seed: seed for random numbers
            @param nsimul: number of simulations per each capacity configuration
            @param capacities: array representing the number of resources per service   
        """
        #self.totalResources = sum(capacities) just to ensure
        self.avgWaitingTime = 0
        self.avgProcessedCount = 0
        self.totalResourceCount = 0
        self.simulations = []
        for seed in seeds:
            #greeter, screener, dispenser, medic]
            simul = PODSimulation.PODSimulation(capacities,
                                                parameterReader)
            simul.model(seed)
            self.simulations.append(simul)
            
        self.resultsAnalyzer = ResultsAnalyzer.ResultsAnalyzer(self.simulations)    
        
        self.avgWaitingTime = self.resultsAnalyzer.get_avg_total_waiting_time()
        self.avgProcessedCount = self.resultsAnalyzer.get_avg_total_number_out()
        self.totalResourceCount = self.resultsAnalyzer.get_total_resources()
        
        
        #simul.plot_stats()
    def get_processed_count(self):
        return self.avgProcessedCount
    def get_resource_count(self):
        return self.totalResourceCount
    def get_avg_waiting_times(self):
        return self.avgWaitingTime
    def get_results_analyzer(self):
        return self.resultsAnalyzer