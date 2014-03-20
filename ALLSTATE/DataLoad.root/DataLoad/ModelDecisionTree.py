#!/usr/bin/python
import pymssql
import numpy as np
import ast
from ConnectionSQL import ConnectionSQL
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
import pandas as pd
import PreProcessing
from OptimiseModelParameters import OptimiseModelParameters
import SharedLibrary
import Context

__modelName = 'DecisionTree'
__featuresColumns = "Pclass, SexINT, SalutationHash, EmbarkedINT, AgeFLOAT, IsChild, IsAdult, HasFamily, HasParent, HasChild, HasSpouse, HasSibling, Parents, Children, Sibling, DeptCodeHash, DeckHash, DualOccupant, OtherSurvivers, HasOtherSurviver, OtherDied, HasOtherDied"
__optimiseParameters = False

def Execute(context):
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

    # 0=DataID, 1=Actual, 2=Pclass, ... 20=A_TitleHash
    # Load Training Data and Cross Validation Data
    train_X, train_Y, train_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="Train", PreProcessDataFrame=__PreProcessDataFrame)
    train_DataID = None

    # Load Cross Validation Data
    cross_X, cross_Y, cross_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="Cross", PreProcessDataFrame=__PreProcessDataFrame)
    cross_DataID = None

    if (__optimiseParameters):
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

    print __modelName + ' criterion=' + criterion + ' max_features=' + str(max_features) + ' max_depth=' + str(max_depth) + ' min_samples_split=' + str(min_samples_split) + ' min_samples_leaf=' + str(min_samples_leaf)
    clf = DecisionTreeClassifier(splitter='best', random_state=1, 
                                 criterion=criterion, max_features=max_features, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
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

    # Feature analysis summary
    featureImportances = enumerate(clf.feature_importances_)
    featureImportanceHistogram = np.array([(importance,train_X.columns[i]) for (i,importance) in featureImportances if importance > 0.01])

    return __modelName, featureImportanceHistogram

def __PreProcessDataFrame(df):
    df['Sex'] = df.apply(lambda row: SharedLibrary.ToMF(row['SexINT']), axis=1)
    df = df.drop(['SexINT'], axis=1)

    df['Embarked'] = df.apply(lambda row: SharedLibrary.ToEmbarked(row['EmbarkedINT']), axis=1)
    df = df.drop(['EmbarkedINT'], axis=1)

    df['Deck'] = df.apply(lambda row: SharedLibrary.ToDeck(row['DeckHash']), axis=1)
    df = df.drop(['DeckHash'], axis=1)

    df['Salutation'] = df.apply(lambda row: SharedLibrary.ToSalutation(row['SalutationHash']), axis=1)
    df = df.drop(['SalutationHash'], axis=1)
    
    df = PreProcessing.OneHotDataframe(df, ['Sex', 'Embarked', 'Deck', 'Salutation'], replace=True)[0] # Convert canonical features to multiple binary features

    #df['DeptCode'] = df.apply(lambda row: SharedLibrary.ToDeptCode(row['DeptCodeHash']), axis=1)
    #df = df.drop(['DeptCodeHash'], axis=1) # Suspected noise
    #df = PreProcessing.OneHotDataframe(df, ['DeptCode'], replace=True)[0] # Convert canonical features to multiple binary features

    #df['Pclass'] = df.apply(lambda row: SharedLibrary.To1st2nd3rd(row['Pclass']), axis=1)
    #df = PreProcessing.OneHotDataframe(df, ['Pclass'], replace=True)[0] # Convert canonical features to multiple binary features

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

    clf = DecisionTreeClassifier(splitter='best', random_state=1, 
                                 criterion=criterion, max_features=max_features, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
    model = clf.fit(train_X, train_Y) # All features must be float.
    accuracy = clf.score(cross_X, cross_Y) # Score=Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct

    return accuracy

