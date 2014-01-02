'''
Created on 02-Jan-2014

@author: blackpearl
'''

class MedAppValueError(Exception):
    '''
    classdocs
    '''


    def __init__(self,value):
        self.value = value;
    
    def __str__(self):
        return repr(self.value)
        