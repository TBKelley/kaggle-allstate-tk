#!/usr/bin/python
import pymssql
import numpy as np
import ast
from ConnectionSQL import ConnectionSQL
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import pandas as pd
import PreProcessing
import SharedLibrary
import Context

__modelName = 'Base'
__featuresColumns = "Pclass, A_TitleHash, SexINT, HasFamily, DeptCodeHash, EmbarkedINT"
#__selectTrainColumns = "DataID, Actual, " + __selectFeaturesColumns
#__selectColumns = "DataID, Actual, " + __selectFeaturesColumns + ", DataType"

#__selectTrainSql = "SELECT " + __selectTrainColumns + " FROM [dbo].[WRK_Train_vw] WHERE [WRK_Train_vw].[DataType] IN (1, 9) ORDER BY [WRK_Train_vw].[DataID]"
#__selectCrossSql = "SELECT " + __selectTrainColumns + " FROM [dbo].[WRK_Train_vw] WHERE [WRK_Train_vw].[DataType] IN (2) ORDER BY [WRK_Train_vw].[DataID]"
#__selectTestSql = "SELECT " + __selectTestColumns + " FROM [dbo].[WRK_Train_vw] WHERE [WRK_Train_vw].[DataType] IN (2) ORDER BY [WRK_Train_vw].[DataID]"
#__selectAllSql = "SELECT " + __selectColumns + " FROM [dbo].[WRK_Train_vw] ORDER BY [WRK_Train_vw].[DataID]"

# Base case described in forum
def Execute(context):
    connectionSQL = ConnectionSQL(context)

    estimators = 1000
    # 0=DataID, 1=Actual, 2=Pclass, ... 7=EmbarkedINT
    # Load Training Data and Cross Validation Data
    train_X, train_Y, train_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="Train", PreProcessDataFrame=__PreProcessDataFrame)
    train_DataID = None

    # Load Cross Validation Data
    cross_X, cross_Y, cross_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="Cross", PreProcessDataFrame=__PreProcessDataFrame)
    cross_DataID = None

    print 'Random Forest Classifier estimators=' + str(estimators)
    clf = RandomForestClassifier(n_estimators = estimators, n_jobs=7, oob_score=True)
    model = clf.fit(train_X, train_Y) # All features must be float.
#    model = clf.fit(train_features, train_result) # All features must be float.
    print ''

    # Training error reports
    SharedLibrary.TrainingError(dataType='Training', modelName=__modelName, clf=clf, model=model, dfX=train_X, dfY=train_Y)
    SharedLibrary.TrainingError(dataType='CrossVal', modelName=__modelName, clf=clf, model=model, dfX=cross_X, dfY=cross_Y)

    # Cross validation report
    #__CrossValidation(clf, train_X, train_Y, n_fold=5)
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

    df['Pclass'] = df.apply(lambda row: SharedLibrary.To1st2nd3rd(row['Pclass']), axis=1)

    df = PreProcessing.OneHotDataframe(df, ['Sex', 'Pclass', 'A_TitleHash', 'DeptCodeHash', 'EmbarkedINT'], replace=True)[0] # Convert canonical features to multiple binary features
    return df 
