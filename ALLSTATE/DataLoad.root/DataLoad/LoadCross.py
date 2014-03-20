#!/usr/bin/python
from ConnectionSQL import ConnectionSQL
import Context

def Execute(context, seed, validationPct):
    connectionSQL = ConnectionSQL(context)

    dataType = '2'
    mssqlColumns = '[DataType],CustomerId,ShoppingPt,RecordType,Day,Time,State,Location,GroupSize,HomeOwner,CarAge,CarValue,RiskFactor,AgeOldest,AgeYoungest,MarriedCouple,CPrevious,DurationPrevious,A,B,C,D,E,F,G,Cost' # No DataID

    if (context.CrossCsvUNC == ""):
        connectionSQL.Execute("EXEC [dbo].[RAW_Data_UPDATE_DataType_Validation_sp] @Seed=" + str(seed)+ ", @ValidationPct=" + str(validationPct)) # Randomally Allocate Validation Data from Training data
    else:
        connectionSQL.RAW_Data_Load(context.CrossCsvUNC, dataType, mssqlColumns)


