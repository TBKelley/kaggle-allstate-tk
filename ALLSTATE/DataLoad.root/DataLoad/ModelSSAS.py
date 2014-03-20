#!/usr/bin/python
from ConnectionSQL import ConnectionSQL
import SharedLibrary
import Context

def Execute(context):
    connectionSQL = ConnectionSQL(context)

    connectionSQL.Execute('EXEC dbo.SSAS_Predict_Ensemble_sp')

