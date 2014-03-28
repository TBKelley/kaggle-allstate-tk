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
    # customer_ID,plan
    resultRow = []
    resultRow.append('customer_ID')
    resultRow.append('plan')
    fileCsv.writerow(resultRow)

    for row in rows:
        customer_ID = row['CustomerId']
        plan = row['Predicted']

        resultRow = []
        resultRow.append(customer_ID)
        resultRow.append(plan)

        fileCsv.writerow(resultRow)

    print 'Output submition file rows=' + str(len(rows)) + ' to ' + fileCsvUNC
    print ''