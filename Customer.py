'''
Created on Sep 23, 2012

@author: ivihernandez
'''
#standard imports
import random
#non standard imports
import SimPy.Simulation as simpy

#ivan's imports



class Customer(simpy.Process):
    """ Customer arrives, looks around and leaves """
    def __init__(self,
                 name,
                 resources,
                 monitors,
                 times,
                 exitResource,
                 exitMonitor,
                 entryResource,
                 entryMonitor,
                 preScreenedPercentage):
        simpy.Process.__init__(self)
        self.resources = resources
        self.monitors = monitors
        self.times = times
        self.exitResource = exitResource
        self.exitMonitor = exitMonitor
        self.entryResource = entryResource
        self.entryMonitor = entryMonitor
        
        self.name = name
        self.generate_forms()
        self.preScreenedPercentage = preScreenedPercentage
        self.set_pre_screening_status(preScreenedPercentage)
    
    def set_pre_screening_status(self, preScreenedPercentage):
        """
            Determine if the person is pre-screened or not
        """
        p = random.random()
        if p <= self.preScreenedPercentage:
            self.preScreened = True
        else:
            self.preScreened = False
        
    def generate_forms(self):
        """
            Determine number and type of forms that the person carries.
            Numbers based on the 
            NYC office of emergency preparedness and response
        """
        p = random.random()
        numberOfForms = 0
        if (p >= 0) and (p <0.318):
            numberOfForms = 1
        elif (p >= 0.318) and (p < 0.586):
            numberOfForms = 2
        elif (p >= 0.586) and (p < 0.749):
            numberOfForms = 3
        elif (p >= 0.749) and (p < 0.875):
            numberOfForms = 4
        elif (p >= 0.875) and (p < 0.943):
            numberOfForms = 5
        else:
            numberOfForms = 6
        
        
        
        p = random.random()
        if (p >= 0) and (p < 0.88):
            formType = 'DOXYCYCLINE'
        elif (p >= 0.88) and (p < 0.99):
            formType = 'CIPROFLOXACIN'
        else:
            formType = 'MEDICAL'
        self.forms = [formType] * numberOfForms
        self.numberOfForms = numberOfForms
        
    def visit(self):
        self.debug = False
        for i in self.visit_entry():#count number in
            yield i 
        
        for i in self.visit_greeter():
            yield i
    
    def visit_entry(self):       
        name = 'entry'
        if self.debug:
            print self.name, "at ",name, simpy.now()
        
        arrive = simpy.now()
        yield simpy.request, self, self.entryResource
        wait = simpy.now() - arrive
        self.entryMonitor.observe(wait)
        tib = 0#random.expovariate(1.0/self.times[name])   
        yield simpy.hold,self,tib
        yield simpy.release, self, self.entryResource
    
    def visit_greeter(self):       
        name = 'greeter'
        if self.debug:
            print self.name, "at ",name, simpy.now()
        
        arrive = simpy.now()
        yield simpy.request, self, self.resources[name]
        wait = simpy.now() - arrive
        self.monitors[name].observe(wait)
        #tib = 0.2#random.expovariate(1.0/self.times[name])
        tib = random.triangular(low=5/60.0, high=92/60.0, mode=23/60.0)
        yield simpy.hold,self,tib
        yield simpy.release, self, self.resources[name]
        p = random.random()
        if self.preScreened:
            for i in self.visit_dispenser():
                yield i
        else:
            for i in self.visit_screener():
                yield i
            
        
        
        
        
         
    def visit_screener(self):
        """
            After cleaning
            
            Aggregated:
            
            Lognormal with:
                logarithmic mean: -2.125
                logarithmic std dev: 0.428
            
            Weibull with:
                shape = 2.29  (beta in python)
                scale = 0.142 (alpha in python)
            
            Separated:
            Medical Screening -> Gamma distribution with
                                 shape: 4.876
                                 rate: 32.55
            Ciprofloxacin Screening -> Gamma distribution with
                                 shape: 6.258
                                 rate: 47.165
            Doxycycline Screening -> Lognormal distribution with
                                logarithmic mean: -2.165
                                logarithmic std dev: 0.413
        """       
        name = 'screener'
        if self.debug:
            print self.name, "at ",name, simpy.now()
        arrive = simpy.now()
        yield simpy.request, self, self.resources[name]
        wait = simpy.now() - arrive
        self.monitors[name].observe(wait)
        #time = random.lognormvariate(mu=-2.125, sigma=0.428)
        time = random.weibullvariate(alpha=0.142, beta=2.29)
        tib = self.numberOfForms * time
        yield simpy.hold,self,tib
        yield simpy.release, self, self.resources[name]
        
        
        if 'MEDIC' in self.forms:
            for i in self.visit_medic():
                yield i
        else:
            for i in self.visit_dispenser():
                yield i
            
    
    def visit_dispenser(self):
        """
            Best fit obtained after cleaning the data:
            Weibull Distribution with:
                shape: 1     (beta in python)
                scale: 0.311 (alpha in python)
        """       
        name = 'dispenser'
        if self.debug:
            print self.name, "at ",name, simpy.now()
        
        arrive = simpy.now()
        yield simpy.request, self, self.resources[name]
        wait = simpy.now() - arrive
        self.monitors[name].observe(wait)
        time = random.weibullvariate(alpha=0.311, beta=1)
        tib = self.numberOfForms * time
        yield simpy.hold,self,tib
        yield simpy.release, self, self.resources[name]
        
        for i in self.visit_exit():
            yield i
        
    
    def visit_medic(self):
        """
            Lognormal with :
            logarithmic mean: 1.024
            logarithmic std dev: 0.788
        """       
        name = 'medic'
        if self.debug:
            print self.name, "at ",name, simpy.now()
        
        arrive = simpy.now()
        yield simpy.request, self, self.resources[name]
        wait = simpy.now() - arrive
        self.monitors[name].observe(wait)
        time = random.lognormvariate(mu=1.024, sigma=0.788) 
        tib = self.numberOfForms * time 
        yield simpy.hold,self,tib
        yield simpy.release, self, self.resources[name]
    
        p = random.random()
        if p < 0.99:
            for i in self.visit_dispenser():
                yield i
        else:
            for i in self.visit_exit():
                yield i
            
        
    def visit_exit(self):       
        name = 'exit'
        if self.debug:
            print self.name, "at ",name, simpy.now()
        
        arrive = simpy.now()
        yield simpy.request, self, self.exitResource
        wait = simpy.now() - arrive
        self.exitMonitor.observe(wait)
        tib = 0#random.expovariate(1.0/self.times[name])   
        yield simpy.hold,self,tib
        yield simpy.release, self, self.exitResource
    
