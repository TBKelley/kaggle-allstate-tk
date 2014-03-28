#!/usr/bin/python
from ConnectionSQL import ConnectionSQL
import SharedLibrary
import Context

# Preload cleanup
def Execute(context):
    connectionSQL = ConnectionSQL(context)

    connectionSQL.TruncateTable("[dbo].[WRK_Customer]")
    connectionSQL.TruncateTable("[dbo].[DRV_Predict]")
    connectionSQL.TruncateTable("[dbo].[WRK_Data]")
    connectionSQL.TruncateTable("[dbo].[RAW_Data]")

    cacheFolderUNC = context.CacheFolderUNC
    SharedLibrary.FindAndRemove(cacheFolderUNC, '.tab')