#!/usr/bin/python
import pymssql
import numpy as np
import ast
from ConnectionSQL import ConnectionSQL
from sklearn import svm
from sklearn import cross_validation
import PreProcessing
from OptimiseModelParameters import OptimiseModelParameters
import SharedLibrary
import Context

__modelName = 'SVM'
__featuresColumns = "Pclass, SexINT, SalutationHash, EmbarkedINT, AgeFLOAT, IsChild, IsAdult, HasFamily, HasParent, HasChild, HasSpouse, HasSibling, Parents, Children, Sibling, DeptCodeHash, DeckHash, DualOccupant, OtherSurvivers, HasOtherSurviver, OtherDied, HasOtherDied"
__optimiseParameters = False

def Execute(context):
    connectionSQL = ConnectionSQL(context)

    kernel = 'linear'
    degree = 3

    # model parameter ranges - used for searching for optimial parameter settings
    kernelList = ['linear','poly','rbf','sigmoid']

    parameterRangeDict = {'kernel':kernelList }

    # 0=DataID, 1=Actual, 2=Pclass, ...
    # Load Training Data and Cross Validation Data
    train_X, train_Y, train_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="Train", PreProcessDataFrame=__PreProcessDataFrame)
    train_DataID = None

    # Load Cross Validation Data
    cross_X, cross_Y, cross_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="Cross", PreProcessDataFrame=__PreProcessDataFrame)
    cross_DataID = None

    if (__optimiseParameters):
        parameterDictMax = {}
        accuracyMax = 0.0

        # package paramaters
        dataDict = {'train_X':train_X, 'train_Y':train_Y, 'cross_X':cross_X, 'cross_Y':cross_Y}

        # Optimal Paramater selection
        # Kernel=Linear
        kernelList = ['linear']
        degreeList = [3]
        parameterRangeDict = {'kernel':kernelList, 'degree':degreeList }
        optimiseModelParameters = OptimiseModelParameters(modelName=__modelName)
        optimiseModelParameters.Percent = 0.2 # 20%
        parameterDict, accuracy = optimiseModelParameters.ExecuteExhaustive(dataDict=dataDict, accuracyFunct=__Accuracy, parameterRangeDict=parameterRangeDict)
        if (accuracy > accuracyMax):
            parameterDictMax = parameterDict
            accuracyMax = accuracy

        # Kernel=poly
        kernelList = ['poly']
        degreeList = [2, 3, 4]
        parameterRangeDict = {'kernel':kernelList, 'degree':degreeList }
        optimiseModelParameters = OptimiseModelParameters(modelName=__modelName)
        optimiseModelParameters.Percent = 0.2 # 20%
        parameterDict, accuracy = optimiseModelParameters.ExecuteExhaustive(dataDict=dataDict, accuracyFunct=__Accuracy, parameterRangeDict=parameterRangeDict)
        if (accuracy > accuracyMax):
            parameterDictMax = parameterDict
            accuracyMax = accuracy

        # Kernel=rbf
        kernelList = ['rbf']
        degreeList = [3]
        parameterRangeDict = {'kernel':kernelList, 'degree':degreeList }
        optimiseModelParameters = OptimiseModelParameters(modelName=__modelName)
        optimiseModelParameters.Percent = 0.2 # 20%
        parameterDict, accuracy = optimiseModelParameters.ExecuteExhaustive(dataDict=dataDict, accuracyFunct=__Accuracy, parameterRangeDict=parameterRangeDict)
        if (accuracy > accuracyMax):
            parameterDictMax = parameterDict
            accuracyMax = accuracy

        # Kernel=sigmoid
        kernelList = ['sigmoid']
        degreeList = [3]
        parameterRangeDict = {'kernel':kernelList, 'degree':degreeList }
        optimiseModelParameters = OptimiseModelParameters(modelName=__modelName)
        optimiseModelParameters.Percent = 0.2 # 20%
        parameterDict, accuracy = optimiseModelParameters.ExecuteExhaustive(dataDict=dataDict, accuracyFunct=__Accuracy, parameterRangeDict=parameterRangeDict)
        if (accuracy > accuracyMax):
            parameterDictMax = parameterDict
            accuracyMax = accuracy

        kernel = parameterDictMax['kernel']
        degree = parameterDictMax['degree']

    print __modelName + 'Classifier'
    clf = svm.SVC(probability=True, verbose=False, random_state=1, kernel=kernel, degree=degree)
    model = clf.fit(train_X, train_Y) # All features must be float.
    print ''

    # Training error reports
    SharedLibrary.TrainingError(dataType='Training', modelName=__modelName, clf=clf, model=model, dfX=train_X, dfY=train_Y)
    SharedLibrary.TrainingError(dataType='CrossVal', modelName=__modelName, clf=clf, model=model, dfX=cross_X, dfY=cross_Y)

    # Cross validation report
    SharedLibrary.CrossValidation(modelName=__modelName, clf=clf, dfX=train_X, dfY=train_Y, n_fold=5)

    # UPDATE DRV_Predict with all data predictions.
    all_X, all_Y, all_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="ALL", PreProcessDataFrame=__PreProcessDataFrame)
    all_Y = None
    connectionSQL.Update_DRV_Predict(modelName=__modelName, model=model, all_X=all_X, all_DataID=all_DataID)

    return __modelName


def __PreProcessDataFrame(df):
    df['Sex'] = df.apply(lambda row: SharedLibrary.ToMF(row['SexINT']), axis=1)
    df = df.drop(['SexINT'], axis=1)

    df['Pclass'] = df.apply(lambda row: SharedLibrary.To1st2nd3rd(row['Pclass']), axis=1)

    df['Embarked'] = df.apply(lambda row: SharedLibrary.ToEmbarked(row['EmbarkedINT']), axis=1)
    df = df.drop(['EmbarkedINT'], axis=1)

    df['Deck'] = df.apply(lambda row: SharedLibrary.ToDeck(row['DeckHash']), axis=1)
    df = df.drop(['DeckHash'], axis=1)

    df['Salutation'] = df.apply(lambda row: SharedLibrary.ToSalutation(row['SalutationHash']), axis=1)
    df = df.drop(['SalutationHash'], axis=1)

    df = PreProcessing.OneHotDataframe(df, ['Sex', 'Pclass', 'Embarked', 'Deck', 'Salutation'], replace=True)[0] # Convert canonical features to multiple binary features

    return df

# Calculate Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct
def __Accuracy(dataDict, parameterDict):
    train_X = dataDict['train_X']
    train_Y = dataDict['train_Y']
    cross_X = dataDict['cross_X']
    cross_Y = dataDict['cross_Y']

    kernel = parameterDict['kernel']
    degree = parameterDict['degree']

    clf = svm.SVC(probability=False, verbose=False, random_state=1, kernel=kernel, degree=degree)
    model = clf.fit(train_X, train_Y) # All features must be float.
    accuracy = clf.score(cross_X, cross_Y) # Score=Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct

    return accuracy

