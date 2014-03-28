#!/usr/bin/python
import pymssql
import numpy as np
import ast
from ConnectionSQL import ConnectionSQL
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import pandas as pd
from TimeStamp import TimeStamp
import PreProcessing
import SharedLibrary
import Context

__modelName = 'Base'
#__featuresColumns = "State,Location,GroupSize,HomeOwner,CarAge,CarValue,RiskFactor,AgeOldest,AgeYoungest,MarriedCouple,CPrevious,DurationPrevious,A,B,C,D,E,F,G,Cost"
__featuresColumns = "A,B,C,D,E,F,G"
__viewName = '[dbo].[WRK_Train_Base_vw]'

# Base Algorithm of using ShoppingPt to predict PurchasePt
def Execute(context):
    timeStamp = TimeStamp()
    connectionSQL = ConnectionSQL(context)

    # 0=DataID, 1=P_A, 2=P_B, 3=P_C, 4=P_D, 5=P_E, 6=P_F, 7=P_G, 8=State, ... 27=Cost
    # Load Training Data and Cross Validation Data
    train_X, train_Y, train_DataID = connectionSQL.GetFeaturesAndResultsFromCache(featuresColumns=__featuresColumns, dataType="Train", modelName=__modelName, preProcessDataFrame=__PreProcessDataFrame, viewName=__viewName)
    train_DataID = None

    # Load Cross Validation Data
    cross_X, cross_Y, cross_DataID = connectionSQL.GetFeaturesAndResultsFromCache(featuresColumns=__featuresColumns, dataType="Cross", modelName=__modelName, preProcessDataFrame=__PreProcessDataFrame, viewName=__viewName)
    cross_DataID = None

    print ''

    clf = BaseClassifier()
    model = clf.fit(train_X, train_Y)

    # Training error reports
    SharedLibrary.TrainingError(dataType='Training', modelName=__modelName, clf=clf, model=model, dfX=train_X, dfY=train_Y)
    SharedLibrary.TrainingError(dataType='CrossVal', modelName=__modelName, clf=clf, model=model, dfX=cross_X, dfY=cross_Y)

    # UPDATE DRV_Predict with all data predictions.
    # TODO: Use SQL Stored procedure to update DRV_Predict for base case
    all_X, all_Y, all_DataID = connectionSQL.GetFeaturesAndResultsFromCache(featuresColumns=__featuresColumns, dataType="ALL", modelName=__modelName, preProcessDataFrame=__PreProcessDataFrame, viewName=__viewName)
    all_Y = None
    connectionSQL.Update_DRV_Predict(modelName=__modelName, model=model, all_X=all_X, all_DataID=all_DataID)

    print __modelName + ' Elaspe=' + timeStamp.Elaspse
    return

def __PreProcessDataFrame(df):
    #df['Sex'] = df.apply(lambda row: SharedLibrary.ToMF(row['SexINT']), axis=1)
    #df = df.drop(['SexINT'], axis=1)

    #df['CarValue'] = df.apply(lambda row: SharedLibrary.ToCarValueINT(row['CarValue']), axis=1)

    #df = PreProcessing.OneHotDataframe(df, ['State', 'Location','CarValue'], replace=True)[0] # Convert canonical features to multiple binary features
    return df 

class BaseClassifier(object):
    """
    Pseudo Classifier for Base.
    """
    def fit(self, dfX, dfY):
        model = ModelBase()
        return model

    def score(self, dfX, dfY): # Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct
        dfCompare = (dfX[['A','B','C','D','E','F','G']] == dfY[['A','B','C','D','E','F','G']])
        correct = dfCompare.apply(lambda row: row['A'] and row['B'] and row['C'] and row['D'] and row['E'] and row['F'] and row['G'], axis=1).astype(np.float).sum()
        count = dfY.shape[0] * 1.0

        return correct/count

class ModelBase(object):
    """
    Pseudo model for Base.
    """
    def predict(self, dfX):
        listY = dfX[['A', 'B', 'C', 'D', 'E', 'F', 'G']].values.tolist()
        return listY