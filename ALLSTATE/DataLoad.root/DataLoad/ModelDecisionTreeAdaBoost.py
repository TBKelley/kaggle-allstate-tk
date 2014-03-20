#!/usr/bin/python
import pymssql
import numpy as np
import ast
from ConnectionSQL import ConnectionSQL
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import cross_validation
import pandas as pd
import PreProcessing
import SharedLibrary
import Context

__modelName = 'DecisionTreeAdaBoost'
__featuresColumns = "Pclass, SexINT, SalutationHash, EmbarkedINT, AgeFLOAT, IsChild, IsAdult, HasFamily, HasParent, HasChild, HasSpouse, HasSibling, Parents, Children, Sibling, DeptCodeHash, DeckHash, DualOccupant, OtherSurvivers, HasOtherSurviver, OtherDied, HasOtherDied"

def Execute(context):
    connectionSQL = ConnectionSQL(context)

    estimators = 3000
    max_features = None
    max_depth = 10
    min_samples_split=5
    min_samples_leaf=5
    bootstrap=True
    n_jobs=-1

    # 0=DataID, 1=Actual, 2=Pclass, ... 
    # Load Training Data and Cross Validation Data
    train_X, train_Y, train_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="Train", PreProcessDataFrame=__PreProcessDataFrame)
    train_DataID = None

    # Load Cross Validation Data
    cross_X, cross_Y, cross_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="Cross", PreProcessDataFrame=__PreProcessDataFrame)
    cross_DataID = None

    # AdaBoost Model
    estimators_AdaBoost = 50
    print 'Decision Tree AdaBoost Classifier estimators=' + str(estimators_AdaBoost)
    tree = DecisionTreeClassifier(criterion='gini', splitter='best', max_features=max_features, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, compute_importances=None)
    clf = AdaBoostClassifier(tree, n_estimators=estimators_AdaBoost, learning_rate=1.0, algorithm='SAMME.R', random_state=None)
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

    df['Pclass'] = df.apply(lambda row: SharedLibrary.To1st2nd3rd(row['Pclass']), axis=1)

    df['Embarked'] = df.apply(lambda row: SharedLibrary.ToEmbarked(row['EmbarkedINT']), axis=1)
    df = df.drop(['EmbarkedINT'], axis=1)

    df['Deck'] = df.apply(lambda row: SharedLibrary.ToDeck(row['DeckHash']), axis=1)
    df = df.drop(['DeckHash'], axis=1)

    df['Salutation'] = df.apply(lambda row: SharedLibrary.ToSalutation(row['SalutationHash']), axis=1)
    df = df.drop(['SalutationHash'], axis=1)

    df = PreProcessing.OneHotDataframe(df, ['Sex', 'Pclass', 'Embarked', 'Deck', 'Salutation'], replace=True)[0] # Convert canonical features to multiple binary features

    return df
