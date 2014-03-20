PRINT 'TRUNCATE LOG FILE.'
PRINT '-------- --- ----'
GO
DECLARE @DatabaseName	sysname
SET @DatabaseName = DB_NAME()
BACKUP LOG @DatabaseName WITH TRUNCATE_ONLY
GO
