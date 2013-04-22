'''
Created on Sep 24, 2012

@author: ivihernandez
'''
#standard imports
import random
#non standard imports
import SimPy.Simulation as simpy
#ivan's imports
import Customer

class Source(simpy.Process):
    """Source generates customers randomly """
    def generate(self, number, 
                 interval, 
                 resources, 
                 monitors, 
                 times,  
                 exitResource, 
                 exitMonitor,
                 entryResource,
                 entryMonitor,
                 preScreenedPercentage):
        """
            @param number: number of entitites to generate (integer)
            @param interval: mean (in minutes) of times inter arrival
            @param resources: array of resources (servers)
            @param monitors:   array of monitors to collect statistics
            @param times: avg. service time depending on the resource
        """
        for i in range(number):
            customerName = "customer%d"%i
            c = Customer.Customer(name=customerName,
                                  resources=resources,
                                  monitors=monitors,
                                  times=times,
                                  exitResource=exitResource,
                                  exitMonitor=exitMonitor,
                                  entryResource=entryResource,
                                  entryMonitor=entryMonitor,
                                  preScreenedPercentage=preScreenedPercentage
                                  )
            
            simpy.activate(c,c.visit())
            
            t = random.expovariate(1.0/interval)
            yield simpy.hold, self, t