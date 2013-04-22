'''
Created on Mar 21, 2013

@author: ivihernandez
'''
#standard imports
from collections import defaultdict
import numpy
import math
from scipy import stats
#ivan's imports
import myutils

def get_half_width(mylist):
        """
            @param mylist: list with multiple measurements 
            Assumptions: 
                1)size larger than 30
                2)normality assumption holds
            @output: half width
        """
        if len(mylist) == 0:
            return 0
        
        mean = numpy.mean(mylist)
        sd = numpy.std(mylist)
        n = len(mylist)
        sdBar = sd/math.sqrt(n)
        df = n - 1
        alpha = 0.05
        
        tHalf = stats.t._ppf(1 - alpha/2.0, df)
        
        E = tHalf * sdBar
        return E

class ResultsAnalyzer:
    def __init__(self, simulations):
        """
            This function takes the average of multiple simulation 
            statistics and averages them in order to obtain a better
            estimate. The statistics analyzed are:
            1) Total Average waiting time
            2) Total Number of resources
            3) Total Number of entities processed
            4) Waiting times per queue
            5) Average number waiting per queue
            6) Utilization per resource
            7) Total Number Seized per resource
            
            
            @param simulations: list of objects of type PODSimulation
             
        """
        self.waiting = defaultdict(float)        #resource -> avg. waiting time
        self.numberWaiting = defaultdict(float)         #resource -> avg. number waiting
        self.utilization = defaultdict(float)    #resource -> avg. utilization
        self.seized = defaultdict(float)         #resource -> avg. number seized
        self.avgTotalNumberOut = 0       #total resources processed
        self.avgTotalNumberIn = 0               #total number in
        self.avgTotalWaitingTime = 0            #total avg. waiting time
        self.totalResources = 0       #total number of resources
        self.capacities = 0         #resources per queue
        
        self.capacities = simulations[0].get_capacities()
        self.totalResources = simulations[0].get_resource_count()
        self.n = len(simulations)
        self.maxTime = simulations[0].maxTime
        n = self.n
        
        numberOut = []          #total number out per simulation
        numberIn = []           #total number in per simulation
        waitingTime = []        #total waiting time per simulaiton
        waitingTimeValues = defaultdict(list)      #total waiting time per simulation per station
        
        numberSeizedValues = defaultdict(list)
        numberWaitingValues = defaultdict(list)
        utilizationValues = defaultdict(list)
        for simul in simulations:
            
            self.avgTotalNumberOut += simul.get_number_out() / float(n)
            self.avgTotalNumberIn += simul.get_number_in() / float(n)
            self.avgTotalWaitingTime += simul.get_avg_waiting_times() / float(n)
            
            numberOut.append(simul.get_number_out())
            numberIn.append(simul.get_number_in())
            waitingTime.append(simul.get_avg_waiting_times())
            
            
            for key in simul.monitors.keys():
                #waiting time
                try:
                    self.waiting[key] += simul.monitors[key].mean() / float(n)
                    waitingTimeValues[key].append(simul.monitors[key].mean())
                except ZeroDivisionError:
                    self.waiting[key] += 0
                    
            for key in simul.resources.keys():
                #number waiting
                self.numberWaiting[key] += simul.get_number_waiting(key) / float(n)#simul.resources[key].waitMon.mean() / float(n)
                numberWaitingValues[key].append(simul.get_number_waiting(key))
                #utilization
                self.utilization[key] += simul.get_utilization(key) /float(n)
                utilizationValues[key].append(simul.get_utilization(key))
                #number seized
                self.seized[key] += simul.monitors[key].count() / float(n)
                numberSeizedValues[key].append(simul.monitors[key].count())
        
        self.halfWidthTotalNumberOut = get_half_width(numberOut)
        self.halfWidthTotalNumberIn = get_half_width(numberIn)
        self.halfWidthTotalWaitingTime = get_half_width(waitingTime) #per simulation
        self.halfWidthWaitingTimes = {}
        self.halfWidthNumberSeized = {}
        self.halfWidthUtilization = {}
        self.halfWidthNumberWaiting = {}
        
        for key in simul.monitors.keys():
            self.halfWidthWaitingTimes[key] = get_half_width(waitingTimeValues[key])
            self.halfWidthNumberSeized[key] = get_half_width(numberSeizedValues[key])
            self.halfWidthNumberWaiting[key] = get_half_width(numberWaitingValues[key])
            self.halfWidthUtilization[key] = get_half_width(utilizationValues[key])
            
        
    def get_total_resources(self):
        return self.totalResources
    def get_avg_total_waiting_time(self):
        return self.avgTotalWaitingTime
    def get_avg_total_number_out(self):
        return self.avgTotalNumberOut
    def get_avg_total_number_in(self):
        return self.avgTotalNumberIn
    """
    def get_half_width_number_in(self):
        return self.halfWidthTotalNumberIn
    def get_half_width_number_out(self):
        return self.halfWidthTotalNumberOut
    """
    def get_total_time(self):
        return self.maxTime
    def show_results(self):
        print "simulation time", self.maxTime
        print "capacities", self.capacities
        print "total resources", self.totalResources
        print "Number In"
        print "Average", "\t", "Half Width" 
        print self.avgTotalNumberIn, "\t", self.halfWidthTotalNumberIn
        print 
        print "Number Out"
        print "Average", "\t", "Half Width"
        print self.avgTotalNumberOut, "\t", self.halfWidthTotalNumberOut
        
        print 
        print "Waiting Time"
        print "Average", "\t", "Half Width"
        print self.avgTotalWaitingTime, "\t", self.halfWidthTotalWaitingTime
        
        print
        print "Waiting times (minutes), half width"
        print "Name", "\t", "Average" , "\t", "Half Width"
        for key in self.waiting.keys():
            print key, "\t", self.waiting[key], "\t", self.halfWidthWaitingTimes[key]
        
        print
        print "Number waiting"
        print "Name", "\t", "Average" , "\t", "Half Width"
        for key in self.numberWaiting.keys():
            print key, "\t", self.numberWaiting[key], "\t", self.halfWidthNumberWaiting[key]
        
        print 
        print "Utilization (Beta test)"
        print "Name", "\t", "Average" , "\t", "Half Width"
        for key in self.utilization.keys():
            print key, "\t", self.utilization[key], "\t", self.halfWidthUtilization[key] 
        
        print 
        print "Number seized"
        print "Name", "\t", "Average" , "\t", "Half Width"
        for key in self.seized.keys():
            print key, "\t", self.seized[key], "\t", self.halfWidthNumberSeized[key]