#!/usr/bin/python
#import pymssql
#import numpy as np
#import ast
#from ConnectionSQL import ConnectionSQL
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.ensemble import AdaBoostClassifier
#from sklearn import cross_validation
#from sklearn.externals import joblib # Used to persist trained classifier to disk
import random
#import PreProcessing
#import SharedLibrary
#import Context

class OptimiseModelParameters():
    """Determine optimal Model parameter settings"""

    def __init__(self, modelName):
        self.__ModelName = modelName
        self.__MinPermutations = 100
        self.__MaxPermutations = 1000
        self.__Permutations = 0
        self.__Percent = 0.01
        self.__ExhaustiveMatches = 0
        self.__ExhaustiveParameterDictMax = {}
        self.__ExhaustiveAccuracyMax = 0

    @property
    def ModelName(self):
        return self.__ModelName

    # Number of possible Permutations in parameterRangeDict
    @property
    def Permutations(self):
        return self.__Permutations

    @property
    def MinPermutations(self):
        return self.__MinPermutations

    # Minimum number of permutations tested.
    # MIN(__MinPermutations, __Permutations) will be tested
    @MinPermutations.setter
    def MinPermutations(self, value):
        self.__MinPermutations = value

    @property
    def MaxPermutations(self):
        return self.__MaxPermutations

    # Minimum number of permutations tested.
    # MIN(__MaxPermutations, __Permutations*Percent) will be tested
    @MaxPermutations.setter
    def MaxPermutations(self, value):
        self.__MaxPermutations = value

    @property
    def Percent(self):
        return self.__Percent

    # Default percent of permulations to test. Deafult 0.01=1%
    @Percent.setter
    def Percent(self, value):
        self.__Percent = value

    ## Determine an optimal set of model parameters by selecting all combinations of parameters.
    ## dataDict =  {'train_X':train_X, 'train_Y':train_Y, 'cross_X':cross_X, 'cross_Y':cross_Y}
    ## accuracyFunct = A cost function that trains using train_X/train_Y and returns the cost of teh cross validation data cost_X/cross_Y.
    ##                 Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct
    ## parameterRangeDict = {'Param1':Param1RangeList, 'Param2':Param2RangeList, ...}
    ##                      Where Param1RangeList = [1, 2, 3, 4]  Param2RangeList = ['A', 'B', 'C'], ...
    ## Returns a dict with optimal parameter values {'Param1':Param1Value, 'Param2':Param2Value, ...}
    ##                      Where Param1Value is a member of Param1RangeList, 
    def ExecuteExhaustive(self, dataDict, accuracyFunct, parameterRangeDict):    
        # Find a good initial set of parameters, trying to avoid local maxima and in the global maxima region.
        self.__ExhaustiveMatches = 0
        self.__ExhaustiveParameterDictMax = {} # Best set of parameter values found todate.
        self.__ExhaustiveAccuracyMax = 0

        # Calculate parameter permutations. We will sample only about 1% of all permutations.
        permutations = 1
        for value in parameterRangeDict.values():
            permutations *= len(value)

        self.Permutations = permutations

        print 'Possible permutations=' + str(permutations)

        # Recursively search for best parameter combination
        self.__SearchParameters(dataDict, accuracyFunct, parameterRangeDict, 0)

        print '' 
        print 'Accuracy=' + str(self.__ExhaustiveAccuracyMax) + ' Tied matches=' + str(self.__ExhaustiveMatches) + ' optima.'
        print self.ModelName + ' ' + self.__ParameterDictToStr(self.__ExhaustiveParameterDictMax)
        print '' 

        return  (self.__ExhaustiveParameterDictMax, self.__ExhaustiveAccuracyMax)

    def __SearchParameters(self, dataDict, accuracyFunct, parameterRangeDict, parameterRangeIndex):
        if (parameterRangeIndex < len(parameterRangeDict)):
            parameterRangeKey = parameterRangeDict.keys()[parameterRangeIndex]
            parameterRangeList = parameterRangeDict[parameterRangeKey]
            for parameterValue in parameterRangeList:
                parameterRestrictedRangeDict = parameterRangeDict.copy()
                parameterRestrictedRangeDict[parameterRangeKey] = [parameterValue]
                self.__SearchParameters(dataDict, accuracyFunct, parameterRestrictedRangeDict, parameterRangeIndex+1)
            return
        else:
            parameterDict = {}
            for parameterName, parameterRangeList in parameterRangeDict.items():
                parameterDict[parameterName] = parameterRangeList[0] # Should only have single element lists

            accuracy = accuracyFunct(dataDict, parameterDict)
            if (accuracy > self.__ExhaustiveAccuracyMax):
                self.__ExhaustiveAccuracyMax = accuracy
                self.__ExhaustiveParameterDictMax = parameterDict
                self.__ExhaustiveMatches = 0
                print ''
                print 'Accuracy=' + str(self.__ExhaustiveAccuracyMax) + ' New Max'
                print self.ModelName + ' ' + self.__ParameterDictToStr(self.__ExhaustiveParameterDictMax)
            elif (accuracy == self.__ExhaustiveAccuracyMax):
                self.__ExhaustiveParameterDictMax = parameterDict
                print self.ModelName + ' ' + self.__ParameterDictToStr(self.__ExhaustiveParameterDictMax)
                self.__ExhaustiveMatches += 1    
            return
  
    ## Determine an optimal set of model parameters using randomly selected combinations of parameters
    ## dataDict =  {'train_X':train_X, 'train_Y':train_Y, 'cross_X':cross_X, 'cross_Y':cross_Y}
    ## accuracyFunct = A cost function that trains using train_X/train_Y and returns the cost of teh cross validation data cost_X/cross_Y.
    ##                 Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct
    ## parameterRangeDict = {'Param1':Param1RangeList, 'Param2':Param2RangeList, ...}
    ##                      Where Param1RangeList = [1, 2, 3, 4]  Param2RangeList = ['A', 'B', 'C'], ...
    ## Returns a dict with optimal parameter values {'Param1':Param1Value, 'Param2':Param2Value, ...}
    ##                      Where Param1Value is a member of Param1RangeList, 
    def ExecuteMoneCarlo(self, dataDict, accuracyFunct, parameterRangeDict):    
        # Find a good initial set of parameters, trying to avoid local maxima and in the global maxima region.
        accuracyMax = 0.0;
        parameterDictMax = {} # Best set of parameter values found todate.

        random.seed()

        # Calculate parameter permutations. We will sample only about 1% of all permutations.
        permutations = 1
        for value in parameterRangeDict.values():
            permutations *= len(value)

        self.Permutations = permutations

        if (permutations*self.Percent > self.MaxPermutations):
            maxIteration = self.MaxPermutations
        elif (permutations < self.MinPermutations):
            maxIteration = permutations
        elif (permutations*self.Percent < self.MinPermutations):
            maxIteration = self.MinPermutations
        else:
            maxIteration = permutations*self.Percent
        maxIteration = int(maxIteration)

        print 'Possible permutations=' + str(permutations) + ' maxIteration=' + str(maxIteration)

        # Monte-carlo search for best parameter combination
        matches = 0
        for iteration in range(1, maxIteration+1):
            # Randomly select a set of parameter values
            parameterDict = {}
            for parameterName, parameterRangeList in parameterRangeDict.items():
                parameterDict[parameterName] = random.sample(parameterRangeList, 1)[0]

            accuracy = accuracyFunct(dataDict, parameterDict)
            if (accuracy > accuracyMax):
                accuracyMax = accuracy
                parameterDictMax = parameterDict
                matches = 0
                print ''
                print 'Accuracy=' + str(accuracyMax) + ' New Max'
                print self.ModelName + '(' + str(iteration) + '/' + str(maxIteration) +') ' + self.__ParameterDictToStr(parameterDictMax)
            elif (accuracy == accuracyMax):
                parameterDictMax = parameterDict
                print self.ModelName + '(' + str(iteration) + '/' + str(maxIteration) +') ' + self.__ParameterDictToStr(parameterDictMax)
                matches += 1

        parameterDictMax = parameterDictMax.copy()  # .copy() appears to change feature order.
        print ''
        print 'Accuracy=' + str(accuracyMax) + ' Monte-Carlo Optima'
        print self.ModelName + '    ' + self.__ParameterDictToStr(parameterDictMax)

        # Use Gradient Decent around Monte-Carlo optima
        print ''
        print 'Check neighborhood of opimal value'
        maxIteration = 20
        iteration = 0
        hasImproved = True
        while (iteration < maxIteration and hasImproved):
            iteration += 1

            parameterDictDeltaMax = parameterDictMax.copy() # Save any good parameter sets during delta processing, as there is no extra cost and may be better than parameterDictNext
            accuracyDeltaMax = accuracyMax

            parameterDictNext = parameterDictMax.copy()
            for parameterName, parameterRangeList in parameterRangeDict.items():
                value = parameterDictMax[parameterName]
                index = parameterRangeList.index(value)

                for delta in [-1, 1]:
                    indexDelta = index + delta
                    if (indexDelta >= len(parameterRangeList)):
                        indexDelta = len(parameterRangeList)-1
                    elif (indexDelta < 0):
                        indexDelta = 0

                    if (indexDelta != index):
                        valueDelta = parameterRangeList[indexDelta]

                        parameterDictDelta = parameterDictMax.copy()
                        parameterDictDelta[parameterName] = valueDelta

                        accuracyDelta = accuracyFunct(dataDict, parameterDictDelta)
                        if (accuracyDelta > accuracyMax):
                            parameterDictNext[parameterName] = valueDelta
                            print ''
                            print 'Accuracy=' + str(accuracyDelta) + ' Delta is better than Max!!'
                            print self.ModelName + '(' + str(iteration) + ') ' + self.__ParameterDictToStr(parameterDictDelta)
                        elif (accuracyDelta == accuracyMax):
                            print self.ModelName + '(' + str(iteration) + ') ' + self.__ParameterDictToStr(parameterDictDelta)
                            matches += 1

                        if (accuracyDelta > accuracyDeltaMax):
                            parameterDictDeltaMax[parameterName] = valueDelta
                            accuracyDeltaMax = accuracyDelta
                            print ''
                            print 'Accuracy=' + str(accuracyDelta) + ' Delta is better than DeltaMax'
                            print self.ModelName + '(' + str(iteration) + ') ' + self.__ParameterDictToStr(parameterDictDeltaMax)
             
            accuracyNext = accuracyFunct(dataDict, parameterDictNext)
            if (accuracyNext <= accuracyMax and accuracyDeltaMax <= accuracyMax):
                hasImproved = False
            else:
                if (accuracyNext >= accuracyDeltaMax):
                    parameterDictMax = parameterDictNext
                    accuracyMax = accuracyNext
                    matches = 0
                    print ''
                    print 'Accuracy=' + str(accuracyMax) + ' New Max from Gradient Decent'
                    print self.ModelName + '(' + str(iteration) + ') ' + self.__ParameterDictToStr(parameterDictMax)
                elif (accuracyNext == accuracyDeltaMax):
                    print self.ModelName + '(' + str(iteration) + ') ' + self.__ParameterDictToStr(parameterDictMax)
                else:
                    parameterDictMax = parameterDictDeltaMax
                    accuracyMax = accuracyDeltaMax
                    matches = 0
                    print ''
                    print 'Accuracy=' + str(accuracyMax) + ' New Max Partial Gradient Decent'
                    print self.ModelName + '(' + str(iteration) + ') ' + self.__ParameterDictToStr(parameterDictMax)

            print '' 
            print 'Accuracy=' + str(accuracyMax) + ' Tied matches=' + str(matches) + ' Iteration ' + str(iteration) + ' optima.'
            print self.ModelName + ' ' + self.__ParameterDictToStr(parameterDictMax)

        print '' 
        print 'Accuracy=' + str(accuracyMax) + ' Tied matches=' + str(matches) + ' optima.'
        print self.ModelName + ' ' + self.__ParameterDictToStr(parameterDictMax)
        print '' 

        return  (parameterDictMax, accuracyMax)

    # Convert a dictionary to a string.
    # parameterDict = {'NameA':a, 'NameB':b}
    # retrun 'NameA=' + str(a) + ' NameB=' + str(b)
    def __ParameterDictToStr(self, parameterDict):
        parameterDictToStr = ''
        prefix = ''
        for key, value in parameterDict.items():
            parameterDictToStr += prefix + key + '=' + str(value)
            prefix = ' '
        return parameterDictToStr
