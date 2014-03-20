#!/usr/bin/python
from ConnectionSQL import ConnectionSQL
import SharedLibrary
import Context

def Execute(context):
    connectionSQL = ConnectionSQL(context)

    connectionSQL.Execute('EXEC dbo.DRV_Predict_INSERT_Ensumble1_sp')
