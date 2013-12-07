'''
Created on 01-Dec-2013

@author: blackpearl
'''

from mongoengine import connect

class ConnectionManager(object):
    '''
    classdocs
    '''

    def __init__(self,connect):
        '''
        Constructor
        '''
        this.connect = connect
    
    def getConnection(self,connect):
        connect.con 
        