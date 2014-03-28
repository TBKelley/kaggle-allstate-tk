#!/usr/bin/python
import pymssql
import SharedLibrary
from ConnectionSQL import ConnectionSQL
import Context

def Execute(context):
    connectionSQL = ConnectionSQL(context)

    connectionSQL.TruncateTable("[dbo].[WRK_Customer]")
    connectionSQL.TruncateTable("[dbo].[WRK_Data]")
    connectionSQL.Execute("EXEC dbo.WRK_Data_INSERT_sp")
    connectionSQL.Execute("EXEC dbo.WRK_Customer_INSERT_sp")
    connectionSQL.Execute("EXEC dbo.WRK_Data_UPDATE_P_DataID_sp")
    connectionSQL.ExecuteAuoCommit("EXEC dbo.TruncateShrinkLog_sp")

    #rowHeader = "INSERT [dbo].[WRK_Data] (DataID,[SexINT]) VALUES\n"
    #rowHeader = "INSERT [dbo].[WRK_Data] (DataID) VALUES\n"
    #rows = connectionSQL.GetRowsDictFromSelect("SELECT * FROM [dbo].[RAW_Data] ORDER BY [DataID]")
    #connectionSQL.Loop_INSERT(rows, rowHeader, __FunctProcessRow)

# Generate SQL to insert a single row, without "(" and ")"
# Derive WRK_Data columns that are difficult to calculate in SQL, like missing values.
def __FunctProcessRow(row, paramDict):
    sql = ""

    DataID = row['DataID']
    #Sex = row['Sex']

    #SexINT = SharedLibrary.SexINT(Sex)

    sql +=  str(DataID)
    #sql += "," + str(SexINT)

    return sql

