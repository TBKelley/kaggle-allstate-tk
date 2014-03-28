#!/usr/bin/python
import pymssql
import numpy as np
from ConnectionSQL import ConnectionSQL
from sklearn.linear_model import Perceptron
import PreProcessing
from OptimiseModelParameters import OptimiseModelParameters
import SharedLibrary
import Context

__modelName = 'Perceptron'
#__featuresColumns = "DataID, Actual, Base, DTree, LogisticR, NBays, NNetwork, SVM, DecisionTree, RandomForest"
__optimiseParameters = True

## Use a Percepron to determine optimal weights for the Ensumble Model

def Execute(context):
    connectionSQL = ConnectionSQL(context)

    penalty = None
    alpha = 0.0001
    fit_intercept = True
    n_iter = 20
    shuffle = False
    eta0 = 1

    # model parameter ranges - used for searching for optimial parameter settings
    penaltyList = ['l1', 'l2', 'elasticnet', None]
    alphaList = [0.1, 0.001, 0.0001, 0.00001]
    fit_interceptList = [True, False]
    n_iterList = [5, 10, 20, 30, 40, 100]
    shuffleList = [False]
    eta0List = [1]

    parameterRangeDict = {'penalty':penaltyList, 'alpha':alphaList, 'fit_intercept':fit_interceptList, 'n_iter':n_iterList, 'shuffle':shuffleList, 'eta0':eta0List }

    # 0=DataID, 1=Actual, 2=Base, ...
    # Load Training Data and Cross Validation Data
    train_X, train_Y, train_DataID = __GetFeaturesAndResults(context=context, connectionSQL=connectionSQL, dataType="Train", preProcessDataFrame=__PreProcessDataFrame)
    train_DataID = None

    # Load Cross Validation Data
    cross_X, cross_Y, cross_DataID = __GetFeaturesAndResults(context=context, connectionSQL=connectionSQL, dataType="Cross", preProcessDataFrame=__PreProcessDataFrame)
    cross_DataID = None

    if (__optimiseParameters):
        parameterDictMax = {}
        accuracyMax = 0.0

        # package paramaters
        dataDict = {'train_X':train_X, 'train_Y':train_Y, 'cross_X':cross_X, 'cross_Y':cross_Y}
        
        optimiseModelParameters = OptimiseModelParameters(modelName=__modelName)
        optimiseModelParameters.Percent = 0.20 # 20%
        parameterDictMax, accuracyMax = optimiseModelParameters.ExecuteMoneCarlo(dataDict=dataDict, accuracyFunct=__Accuracy, parameterRangeDict=parameterRangeDict)

        penalty = parameterDictMax['penalty']
        alpha = parameterDictMax['alpha']
        fit_intercept = parameterDictMax['fit_intercept']
        n_iter = parameterDictMax['n_iter']
        shuffle = parameterDictMax['shuffle']
        eta0 = parameterDictMax['eta0']

    print __modelName + 'Classifier'
    clf = Perceptron(penalty=penalty, alpha=alpha, fit_intercept=fit_intercept, n_iter=n_iter, shuffle=shuffle, random_state=1, eta0=eta0, warm_start=False)
    model = clf.fit(train_X, train_Y) # All features must be float.
    print ''

    # Training error reports
    SharedLibrary.TrainingError(dataType='Training', modelName=__modelName, clf=clf, model=model, dfX=train_X, dfY=train_Y)
    SharedLibrary.TrainingError(dataType='CrossVal', modelName=__modelName, clf=clf, model=model, dfX=cross_X, dfY=cross_Y)

    # Cross validation report
    SharedLibrary.CrossValidation(modelName=__modelName, clf=clf, dfX=train_X, dfY=train_Y, n_fold=5)

    weights = clf.coef_[0]  # narray
    weights = weights/sum(weights)
    modelNames = train_X.keys();
    weightsDict = {}
    for index in range(len(modelNames)):
        weightsDict[modelNames[index]] = weights[index]

    weightsString = ''
    prefix = ''
    for key, value in weightsDict.iteritems():
        weightsString += prefix + key + '=' + str(value)
        prefix = ' '

    print 'Weights ' + weightsString
    print ''

    # UPDATE DRV_Predict with all data predictions.
    all_X, all_Y, all_DataID = __GetFeaturesAndResults(context=context, connectionSQL=connectionSQL, dataType="ALL", preProcessDataFrame=__PreProcessDataFrame)
    all_Y = None
    connectionSQL.Update_DRV_Predict(modelName=__modelName, model=model, all_X=all_X, all_DataID=all_DataID)

    return __modelName

# Get Feature Dataform (dfX), Results Series (dfY) and DataID Series (dfDataID)
# featuresColumns = Example: "Pclass, A_TitleHash"
# dataType = "Train"=(1,9), "Cross"=(2), "Test"=(3) or ALL=(*)
# PreProcessDataFrame = Function used to modify and pre-process columns. Signature df=PreProcessDataFrame(df)
def __GetFeaturesAndResults(context, connectionSQL, dataType, PreProcessDataFrame):
    # Columns: DataID, Actual, Base, DTree, LogisticR, NBays, NNetwork, SVM, DecisionTree, RandomForest, DataType
    selectSql = "EXEC dbo.DRV_Predict_Percepron_LOAD_sp"

    df = connectionSQL.GetRowsDataFrameFromSelect(selectSql)
    df = PreProcessDataFrame(df) # Column manipulation for model

    # Filter required DataType
    if (dataType == "Train"):
        df = df[(df.DataType == 1) | (df.DataType == 9)]
    elif (dataType == "Cross"):
        df = df[(df.DataType == 2)]
    elif (dataType == "Test"):
        df = df[(df.DataType == 3)]

    df = df.drop(['DataType'], axis=1)

    dfDataID = df['DataID']
    dfY = df['Actual'].astype(np.float)
    dfX = df.drop(['DataID', 'Actual'], axis=1).astype(np.float) 
    df = None
    print '  ' + dataType + '_X = ' + str(dfX.shape)
    print '  ' + dataType + '_Y = ' + str(dfY.shape)
    print '  ' + dataType + '_DataID = ' + str(dfDataID.shape)

    return (dfX, dfY, dfDataID) 

## Convert probabilities to predictions
## Base, DTree, LogisticR, NBays, NNetwork, SVM, DecisionTree, RandomForest
def __PreProcessDataFrame(df):
    df['Base'] = df.apply(lambda row: SharedLibrary.ToPrediction(row['Base']), axis=1)
    df['DTree'] = df.apply(lambda row: 1.0 if row['DTree'] >=0.5 else 0.0, axis=1)
    df['LogisticR'] = df.apply(lambda row: 1.0 if row['LogisticR'] >=0.5 else 0.0, axis=1)
    df['NBays'] = df.apply(lambda row: 1.0 if row['NBays'] >=0.5 else 0.0, axis=1)
    df['NNetwork'] = df.apply(lambda row: 1.0 if row['NNetwork'] >=0.5 else 0.0, axis=1)
    df['SVM'] = df.apply(lambda row: 1.0 if row['SVM'] >=0.5 else 0.0, axis=1)
    df['DecisionTree'] = df.apply(lambda row: 1.0 if row['DecisionTree'] >=0.5 else 0.0, axis=1)
    df['RandomForest'] = df.apply(lambda row: 1.0 if row['RandomForest'] >=0.5 else 0.0, axis=1)

    df = df.drop(['Base'], axis=1)
    #df = df.drop(['DTree'], axis=1)
    df = df.drop(['LogisticR'], axis=1)
    df = df.drop(['NBays'], axis=1)
    df = df.drop(['NNetwork'], axis=1)
    #df = df.drop(['SVM'], axis=1)
    df = df.drop(['DecisionTree'], axis=1)
    #df = df.drop(['RandomForest'], axis=1)
    return df

# Calculate Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct
def __Accuracy(dataDict, parameterDict):
    train_X = dataDict['train_X']
    train_Y = dataDict['train_Y']
    cross_X = dataDict['cross_X']
    cross_Y = dataDict['cross_Y']

    penalty = parameterDict['penalty']
    alpha = parameterDict['alpha']
    fit_intercept = parameterDict['fit_intercept']
    n_iter = parameterDict['n_iter']
    shuffle = parameterDict['shuffle']
    eta0 = parameterDict['eta0']

    clf = Perceptron(penalty=penalty, alpha=alpha, fit_intercept=fit_intercept, n_iter=n_iter, shuffle=shuffle, random_state=1, eta0=eta0, warm_start=False)
    model = clf.fit(train_X, train_Y) # All features must be float.
    accuracy = clf.score(cross_X, cross_Y) # Score=Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct

    return accuracy

