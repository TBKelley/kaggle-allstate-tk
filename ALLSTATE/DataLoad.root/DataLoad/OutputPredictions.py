#!/usr/bin/python
import csv as csv
from ConnectionSQL import ConnectionSQL
import SharedLibrary
import Context

def Execute(context, Model):
    fileCsvUNC = context.PredictionCsvUNC.replace('.csv', '_' + Model + '.csv')
    connectionSQL = ConnectionSQL(context)

    fileCsv = csv.writer(open(fileCsvUNC, "wb"))

    # Columns: Model,PassengerId,Predicted,Probablity
    rows = connectionSQL.GetRowsDictFromSelect("EXEC dbo.DRV_Predict_LOAD_sp @Model='" + Model + "'")

    # Write out header
    # Survived,PassengerId
    resultRow = []
    resultRow.append('Survived')
    resultRow.append('PassengerId')
    fileCsv.writerow(resultRow)

    for row in rows:
        Survived = row['Predicted']
        PassengerId = row['PassengerId']

        resultRow = []
        resultRow.append(int(Survived))
        resultRow.append(PassengerId)
        fileCsv.writerow(resultRow)

    print 'Output submition file rows=' + str(len(rows)) + ' to ' + fileCsvUNC
    print ''