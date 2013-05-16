'''
Created on May 15, 2013

@author: ivihernandez
'''
#standard imports

#third-party imports

#my own imports

class ParameterReader:
    def __init__(self, experimentFilePath):
        """
            @param experimentFolderPath: folder containing a list of files.
                Each file contains the parameters needed to run the experiments
        """
        self.parameters = {}
        file = open(experimentFilePath, 'r')
        for line in file:
            elements = line.split(':')
            self.parameters[elements[0]] = elements[1]
    def get_parameter(self, parameterName):
        """
            @param parameterName: name of the parameter of interest
            (e.g. screeningRatio)
            @precondition: the experiment file that contains the parameter of interest
            should have been loaded in memory via the function load_experiment 
        """
        return self.parameters[parameterName]