#!/usr/bin/python
import argparse
import LoadCleanup
import LoadTrain
import LoadCross
import LoadTest
import WRK_Data_POPULATE
import ModelBase
import ModelDecisionTree
import ModelDecisionTreeAdaBoost
import ModelRandomForest
import ModelSVM
import ProcessSSAS
import ModelSSAS
import FeatureAnalysis
import InsertEnsumble_1
import PercepronWeights
import OutputPredictions
from Context import Context

if __name__ == '__main__':
    context = Context()
    seed = 0
    reloadDatabase = context.ReloadDatabase
    validationPct = 0.2 # Percent of training data to be used for cross validation. 0.2 if you are not using CrossCsvUNC

    if (reloadDatabase):
        print ''
        print '---- Preload Cleanup ----'
        LoadCleanup.Execute(context) 
        print ''
        print '---- LoadTrain ----'
        LoadTrain.Execute(context, seed, validationPct) # 
        print ''
        print '---- LoadCross ----'
        LoadCross.Execute(context, seed, validationPct) # 
        print ''
        print '---- LoadTest ----'
        LoadTest.Execute(context)
        print ''
        print '---- Populate WRK_DATA and WRK_Customer, Missing & Derived Data ----'
        WRK_Data_POPULATE.Execute(context)

    print ''
    print '---- ModelBase ----'
    #ModelBase.Execute(context)
    print ''
    print '---- ModelDecisionTree ----'
    modelName, featureImportanceHistogram = ModelDecisionTree.Execute(context)
    print ''
    print '---- FeatureAnalysis - ModelDecisionTree ----'
    FeatureAnalysis.Execute(modelName, featureImportanceHistogram)
    print ''
    print '---- ModelDecisionTreeAdaBoost ----'
    #modelName, featureImportanceHistogram = ModelDecisionTreeAdaBoost.Execute(context)
    print ''
    print '---- FeatureAnalysis - ModelDecisionTreeAdaBoost ----'
    #FeatureAnalysis.Execute(modelName, featureImportanceHistogram)
    print ''
    print '---- ModelRandomForest ----'
    #modelName, featureImportanceHistogram = ModelRandomForest.Execute(context)
    print ''
    print '---- FeatureAnalysis - ModelRandomForest ----'
    #FeatureAnalysis.Execute(modelName, featureImportanceHistogram)
    print ''
    print '---- ModelSVM ----'
    #modelName = ModelSVM.Execute(context)
    print ''
    print '---- ProcessSSAS ----'
    #ProcessSSAS.Execute(context)
    print ''
    print '---- ModelSSAS ----'
    #ModelSSAS.Execute(context)
    print ''
    print '---- DRV_Predict_INSERT_Ensumble1_sp ----'
    #InsertEnsumble_1.Execute(context)
    print ''
    print '---- PercepronWeights ----'
    #modelName = PercepronWeights.Execute(context)
    print '---- OutputPredictions ----'
    OutputPredictions.Execute(context, 'Base')
    OutputPredictions.Execute(context, 'DecisionTree')
    #OutputPredictions.Execute(context, 'RandomForest')
    #OutputPredictions.Execute(context, 'Ensemble')
    #OutputPredictions.Execute(context, 'DTree')
    #OutputPredictions.Execute(context, 'LogisticR')
    #OutputPredictions.Execute(context, 'NNetwork')
    #OutputPredictions.Execute(context, 'Perceptron')
    pass



