from sklearn.tree import DecisionTreeClassifier

class DecisionTreeClassifierMultiClass(DecisionTreeClassifier):
    """Super class for DecisionTreeClassifier"""

    # Override DecisionTreeClassifier.score() as it does not support multiclass
    # Score=Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct
    def score(self, dfX, dfY):
        # dfY.values.tolist() = actual[row] = [A_Lable=1, B_Lable=0, ..., G_Lable=1]
        # Example: actualListOfLists=[[1L, 0L, 2L, 2L, 1L, 2L, 1L], [0L, 0L, 3L, 2L, 0L, 0L, 2L], ...] 
        actualListOfLists = dfY.values.tolist()

        # predicted[row] =[A_Lable=1.0, B_Lable=0.0, ..., G_Lable=3.0]
        # Example: predictedListOfLists = [[1.0, 1.0, 2.0, 2.0, 1.0, 2.0, 1.0], [1.0, 0.0, 3.0, 3.0, 0.0, 0.0, 1.0],  ...]
        predictedListOfLists = self.predict(dfX).tolist()

        # NOTE: [1, 2, 3] == [1.0, 2.0, 3.0] is True
        # Example: haveMatchList=[False, False, False, False, False, ...]
        haveMatchList = [actualRow == predictedRow for actualRow, predictedRow in zip(actualListOfLists, predictedListOfLists)] # [True, False, True, ...]
        matchedRows = sum(haveMatchList) # Example: 171
        countRows = len(haveMatchList) # Example: 1177
        score = matchedRows * 1.0 /countRows # Example: 0.14528462192013594

        return score


