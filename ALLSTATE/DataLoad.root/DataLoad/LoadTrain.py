#!/usr/bin/python
from ConnectionSQL import ConnectionSQL
import Context

def Execute(context, seed, validationPct):
    connectionSQL = ConnectionSQL(context)

    connectionSQL.TruncateTable("[dbo].[DRV_Predict]")
    connectionSQL.TruncateTable("[dbo].[WRK_Data]")
    connectionSQL.TruncateTable("[dbo].[RAW_Data]")

    dataType = '1'
    mssqlColumns = '[DataType],CustomerId,ShoppingPt,RecordType,Day,Time,State,Location,GroupSize,HomeOwner,CarAge,CarValue,RiskFactor,AgeOldest,AgeYoungest,MarriedCouple,CPrevious,DurationPrevious,A,B,C,D,E,F,G,Cost' # No DataID
    connectionSQL.RAW_Data_Load(context.TrainCsvUNC, dataType, mssqlColumns)


