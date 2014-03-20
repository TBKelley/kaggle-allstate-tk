IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.TruncateShrinkLog_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.TruncateShrinkLog_sp
GO

/**************************************************
File: UTL_TruncateShrinkLog_sp.sql

Description: Truncate and Shrink log file after a load

History:
2014-03-19    TrKelley  Created
**************************************************/
CREATE PROCEDURE dbo.TruncateShrinkLog_sp
AS
SET NOCOUNT ON -- Required for VBA
DECLARE @SpName     sysname -- Stored Procedure Name used in error messages
DECLARE @Error      INT
DECLARE @ErrorMsg   NVARCHAR(1024)
SET @SpName = OBJECT_NAME(@@PROCID)
SET @Error = 0
SET @ErrorMsg = NULL

-- Truncate Log File
DECLARE @DatabaseName	sysname
SET @DatabaseName = DB_NAME()
--BACKUP LOG @DatabaseName WITH TRUNCATE_ONLY

-- Shrink the truncated log file to 1 MB.
DBCC SHRINKFILE (ALLSTATE_Log, 1)
DBCC SHRINKFILE (ALLSTATE, 1)

GO

GRANT EXEC, VIEW DEFINITION ON dbo.TruncateShrinkLog_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.TruncateShrinkLog_sp

-- Get Filename. Example: <Database>_Log
SELECT name, * FROM sys.database_files
*****************************************************/

