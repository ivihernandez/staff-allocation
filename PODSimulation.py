'''
Created on Sep 24, 2012

@author: ivihernandez
'''
#standard imports
import random
from collections import defaultdict
import operator
#non standard imports
import SimPy.Simulation as simpy
import SimPy.SimPlot as simplot
import numpy
import math
from scipy import stats
import sys
#ivan's imports

import Source
import ResultsAnalyzer


class PODSimulation:
    def __init__(self, capacities, parameterReader=None):
        self.maxTime = 60# 24*60=1440 minutes
        self.maxNumber = 500000 #entities
        self.meanTBA = 1/200.0#1/float(115) #mean time between arrivals, minutes btw entities
        
        self.capacities = capacities
        self.parameterReader = parameterReader
        
        
        if parameterReader==None:
            self.preScreenedPercentage = 0.1
        else:
            self.preScreenedPercentage = self.parameterReader.get_parameter('preScreenedPercentage')
        #print 'percentage', self.preScreenedPercentage 
        
        #positions = [greeter, screener, dispenser, medic]
        self.resources = {} #resource name -> resource
        self.monitors = {} #resource name -> monitor
        self.times = {} #resource name -> avg. time
        
        ylab = 'designees'
        ########################
        name = 'greeter'
        n = 0
        self.resources[name] = simpy.Resource(capacity=capacities[n], 
                                             name=name,
                                             monitored=True)
        self.monitors[name] = simpy.Monitor(name=name, ylab=ylab)
        
        ########################
        name = 'screener'
        n = 1
        self.resources[name] = simpy.Resource(capacity=capacities[n], 
                                             name=name,
                                             monitored=True)
        self.monitors[name] = simpy.Monitor(name=name, ylab=ylab)
        
        ########################        
        name = 'dispenser'
        n = 2
        self.resources[name] = simpy.Resource(capacity=capacities[n], 
                                             name=name,
                                             monitored=True)        
        self.monitors[name] = simpy.Monitor(name=name, ylab=ylab)
        
        ########################
        name = 'medic'
        n = 3
        self.resources[name] = simpy.Resource(capacity=capacities[n], 
                                             name=name,
                                             monitored=True)
        self.monitors[name] = simpy.Monitor(name=name, ylab=ylab)
        
        
        
        ########################
        name = 'exit'
        self.exitResource = simpy.Resource(capacity=1,name=name)
        self.exitMonitor = simpy.Monitor(name=name, ylab=ylab)
        self.exitTime = 0
        
        #########################
        name = 'entry'
        self.entryResource = simpy.Resource(capacity=1,name=name)
        self.entryMonitor = simpy.Monitor(name=name, ylab=ylab)
        self.entryTime = 0
    def get_capacities(self):
        return self.capacities
    def model(self, seed):
        random.seed(seed)
        
        
        simpy.initialize()
        
        source = Source.Source('Source')
        simpy.activate(source, 
                       source.generate(number=self.maxNumber,
                                       interval=self.meanTBA,
                                       resources=self.resources,
                                       monitors=self.monitors,
                                       times=self.times,
                                       exitResource=self.exitResource,
                                       exitMonitor=self.exitMonitor,
                                       entryResource=self.entryResource,
                                       entryMonitor=self.entryMonitor,
                                       preScreenedPercentage=self.preScreenedPercentage
                                        ),
                      at=0.0
                    )
        simpy.simulate(until=self.maxTime)
        
        
    
    def get_avg_waiting_times(self):
        """
            get avg. waiting time per service
        """
        sum = 0
        for key in self.monitors.keys():
            try:
                value = self.monitors[key].mean()
            except ZeroDivisionError:
                value = 0
            sum += value
            
        
        return sum
    
    def get_resource_count(self):
        sum = 0
        for key in self.resources.keys():
            value = self.resources[key].capacity
            sum += value
        return sum
    def get_number_out(self):
        return self.exitMonitor.count()
    def get_number_in(self):
        return self.entryMonitor.count()
    
    def plot_stats(self):
        plt = simplot.SimPlot()
        plt.plotStep(self.monitors['greeter'],color='blue')
        plt.plotStep(self.monitors['screener'],color='red')
        plt.plotStep(self.monitors['dispenser'],color='green')
        plt.plotStep(self.monitors['medic'],color='purple')
        plt.mainloop()
    def get_number_waiting(self, key):
        """
            Return the average number of people waiting for the resource
            named "key". This is a weighted average, weighted by
            the amount of time in which the queue had a given size.
            
            @param key: name of the queue 
        """
        monitor = self.resources[key].waitMon #list of [time, size]
        
        waiting = defaultdict(float)
        total = 0
        for i in range(len(monitor)):
            if i == 0:
                continue
            timeSpan = monitor[i][0] - monitor[i - 1][0]
            index = monitor[i - 1][1]
            waiting[index] += timeSpan
            total += timeSpan * index
        #include last state of the queue
        
        timeSpan = self.maxTime - monitor[len(monitor) - 1][0]
        index = monitor[len(monitor) - 1][1]
        waiting[index] += timeSpan
        total += timeSpan * index
        ret = total / float(self.maxTime)
        return ret
        
        
        
        #simpy
        """
        simPyRet = self.resources[key].waitMon.timeAverage()
        if simPyRet == None:
            #print self.resources[key].waitMon
            simPyRet = 0.0
        """
        
        
        
    def get_utilization(self, key):
        """
            @param key: name of the queue
             
        """
        """
            Not implemented yet
            See: 
            http://simpy.sourceforge.net/SimPyDocs/Manual.html
            http://simpy.sourceforge.net/SimPyDocs/Manual.html#recording-resource-queue-lengths
            
            for possible solutions
        """
        return 0
        """
        #print "active queue",self.resources[key].activeQ
        val = self.resources[key].actMon.timeAverage()
        if val == None:
            val = 0
        return val
        """
        
        monitor = self.resources[key].waitMon #list of [time, size]
        waiting = defaultdict(float)
        total = 0
        for i in range(len(monitor)):
            if i == 0:
                continue
            index = monitor[i - 1][1]
            if index == 0:
                continue
            timeSpan = monitor[i][0] - monitor[i - 1][0]
            waiting[index] += timeSpan
            total += timeSpan 
        #include last state of the queue
        index = monitor[len(monitor) - 1][1]
        if index != 0:
            timeSpan = self.maxTime - monitor[len(monitor) - 1][0]
            waiting[index] += timeSpan
            total += timeSpan 
        ret = total / float(self.maxTime)
        
        #print "Ivan", ret
        #ret = self.resources[key].waitMon.timeAverage()
        
        #print "SimPy", ret
        
        
        return ret
        
          



def get_10_seeds():
    seeds = [2308947, 
             982301, 
             329, 
             12389, 
             34324,
             45645,
             45456546,
             681683,
             7,
             543]
    return seeds
def get_20_seeds():
    seeds = [2308947, 
             982301, 
             329, 
             12389, 
             34324,
             45645,
             45456546,
             681683,
             7,
             543,
             3982473289,
             1321,
             798789,
             8809,
             35797,
             43,
             879,
             32432,
             78987,
             675489]
    return seeds


        
         
if __name__ == '__main__':
    #greeter, screener, dispenser, medic
    print "program started"
    #capacities = [1,1,1,1]
    capacities = [4, 6, 6, 1]
    
    seeds = get_20_seeds()
    #seeds = [123]
    simulations = []
    for seed in seeds:
        simul = PODSimulation(capacities)
        simul.model(seed)
        simulations.append(simul)
    resultsAnalyzer = ResultsAnalyzer.ResultsAnalyzer(simulations)
    resultsAnalyzer.show_results()
    print "program finished"