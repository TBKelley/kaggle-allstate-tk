#!/usr/bin/python
import pymssql
import numpy as np
import ast
from ConnectionSQL import ConnectionSQL
from sklearn.tree import DecisionTreeClassifier
from DecisionTreeClassifierMultiClass import DecisionTreeClassifierMultiClass
from sklearn import cross_validation
import pandas as pd
from TimeStamp import TimeStamp
import PreProcessing
from OptimiseModelParameters import OptimiseModelParameters
import SharedLibrary
import Context

__modelName = 'DecisionTree'
#__featuresColumns = "State,Location,GroupSize,HomeOwner,CarAge,CarValue,RiskFactor,AgeOldest,AgeYoungest,MarriedCouple,CPrevious,DurationPrevious,A,B,C,D,E,F,G,Cost"
__featuresColumns = "State,Location,GroupSize,HomeOwner,CarAge,CarValue,RiskFactor,AgeOldest,AgeYoungest,MarriedCouple,CPrevious,DurationPrevious,Cost"
__viewName = '[dbo].[WRK_Train_OnlyLastShoppingPt_vw]'
__optimiseParameters = False

def Execute(context):
    timeStamp = TimeStamp()
    connectionSQL = ConnectionSQL(context)

    criterion = 'gini'
    max_features = None
    max_depth = 14
    min_samples_split=6
    min_samples_leaf=6
    n_jobs=-1

    # model parameter ranges - used for searching for optimial parameter settings
    criterionList = ['gini', 'entropy']
    max_featuresList = [7, 8, 9, 10, 11, 12, 13, 14, None]
    max_depthList = [6, 8, 10, 11, 12, 13, 14, None]
    min_samples_splitList = [3, 5, 6, 7, 8, 9]
    min_samples_leafList = [3, 4, 5, 6, 7]
    parameterRangeDict = {'criterion':criterionList, 'max_features':max_featuresList, 'max_depth':max_depthList, 'min_samples_split':min_samples_splitList, 'min_samples_leaf':min_samples_leafList }

    timeStamp1 = TimeStamp('Loading X, Y')
    # 0=DataID, 1=P_A, 2=P_B, 3=P_C, 4=P_D, 5=P_E, 6=P_F, 7=P_G, 8=State, ... 27=Cost
    # Load Training Data and Cross Validation Data
    train_X, train_Y, train_DataID = connectionSQL.GetFeaturesAndResultsFromCache(featuresColumns=__featuresColumns, dataType="Train", modelName=__modelName, preProcessDataFrame=__PreProcessDataFrame, viewName=__viewName)
    train_DataID = None

    # Load Cross Validation Data
    cross_X, cross_Y, cross_DataID = connectionSQL.GetFeaturesAndResultsFromCache(featuresColumns=__featuresColumns, dataType="Cross", modelName=__modelName, preProcessDataFrame=__PreProcessDataFrame, viewName=__viewName)
    cross_DataID = None

    print '  Elaspe=' + timeStamp1.Elaspse
    print ''

    if (__optimiseParameters):
        timeStamp1 = TimeStamp('Optimise parameters')
        # package paramaters
        dataDict = {'train_X':train_X, 'train_Y':train_Y, 'cross_X':cross_X, 'cross_Y':cross_Y}

        # Optimal Paramater selection
        #parameterDictMax = __OptimalParamaterSelection(dataDict=dataDict, accuracyFunct=__Accuracy, parameterRangeDict=parameterRangeDict)
        optimiseModelParameters = OptimiseModelParameters(modelName=__modelName)
        optimiseModelParameters.Percent = 0.2 # 20%
        parameterDictMax, accuracyMax = optimiseModelParameters.ExecuteMoneCarlo(dataDict=dataDict, accuracyFunct=__Accuracy, parameterRangeDict=parameterRangeDict)

        criterion = parameterDictMax['criterion']
        max_features = parameterDictMax['max_features']
        max_depth = parameterDictMax['max_depth']
        min_samples_split = parameterDictMax['min_samples_split']
        min_samples_leaf = parameterDictMax['min_samples_leaf']

        print 'Elaspe=' + timeStamp1.Elaspse
        print ''

    timeStamp1 = TimeStamp('Fit model')
    print __modelName + ' criterion=' + criterion + ' max_features=' + str(max_features) + ' max_depth=' + str(max_depth) + ' min_samples_split=' + str(min_samples_split) + ' min_samples_leaf=' + str(min_samples_leaf)
    clf = DecisionTreeClassifierMultiClass(splitter='best', random_state=1, 
                                           criterion=criterion, max_features=max_features, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
    model = clf.fit(train_X, train_Y) # All features must be float.
    print 'Elaspe=' + timeStamp1.Elaspse 
    print ''

    # Training error reports
    SharedLibrary.TrainingError(dataType='Training', modelName=__modelName, clf=clf, model=model, dfX=train_X, dfY=train_Y)
    SharedLibrary.TrainingError(dataType='CrossVal', modelName=__modelName, clf=clf, model=model, dfX=cross_X, dfY=cross_Y)

    # Cross validation report
    SharedLibrary.CrossValidation(modelName=__modelName, clf=clf, dfX=train_X, dfY=train_Y, n_fold=5)

    # UPDATE DRV_Predict with all data predictions.
    timeStamp1 = TimeStamp('Update_DRV_Predict')
    all_X, all_Y, all_DataID = connectionSQL.GetFeaturesAndResultsFromCache(featuresColumns=__featuresColumns, dataType="ALL", modelName=__modelName, preProcessDataFrame=__PreProcessDataFrame, viewName=__viewName)
    all_Y = None
    connectionSQL.Update_DRV_Predict(modelName=__modelName, model=model, all_X=all_X, all_DataID=all_DataID)
    print 'Elaspe=' + timeStamp1.Elaspse
    print ''

    # Feature analysis summary
    featureImportances = enumerate(clf.feature_importances_)
    featureImportanceHistogram = np.array([(importance,train_X.columns[i]) for (i,importance) in featureImportances if importance > 0.01])

    print __modelName + ' Elaspe=' + timeStamp.Elaspse
    return __modelName, featureImportanceHistogram

def __PreProcessDataFrame(df):
    #df['DOW'] = df.apply(lambda row: SharedLibrary.ToDOW(row['Day']), axis=1)
    #df = df.drop(['Day'], axis=1)
    
    df = PreProcessing.OneHotDataframe(df, ['CarValue'], replace=True)[0] # Specifiy all possible values   
    df = PreProcessing.OneHotDataframe(df, ['State'], replace=True)[0] # Convert canonical features to multiple binary features

    #df['DeptCode'] = df.apply(lambda row: SharedLibrary.ToDeptCode(row['DeptCodeHash']), axis=1)
    #df = df.drop(['DeptCodeHash'], axis=1) # Suspected noise
    #df = PreProcessing.OneHotDataframe(df, ['DeptCode'], replace=True)[0] # Convert canonical features to multiple binary features

    return df

# Calculate Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct
def __Accuracy(dataDict, parameterDict):
    train_X = dataDict['train_X']
    train_Y = dataDict['train_Y']
    cross_X = dataDict['cross_X']
    cross_Y = dataDict['cross_Y']

    criterion = parameterDict['criterion']
    max_features = parameterDict['max_features']
    max_depth = parameterDict['max_depth']
    min_samples_split = parameterDict['min_samples_split']
    min_samples_leaf = parameterDict['min_samples_leaf']

    clf = DecisionTreeClassifierMultiClass(splitter='best', random_state=1, 
                                           criterion=criterion, max_features=max_features, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
    model = clf.fit(train_X, train_Y) # All features must be float.
    accuracy = clf.score(cross_X, cross_Y) # Score=Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct

    return accuracy

