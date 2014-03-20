PRINT 'Compress and Shrink all database files.'
PRINT '-------- --- ------ --- -------- ------'
GO
SET NOCOUNT ON

-- Source table fields
DECLARE  @name          sysname
        ,@physical_name sysname

DECLARE Record_cursor CURSOR FORWARD_ONLY READ_ONLY FOR
SELECT   master_files.name
        ,master_files.physical_name
FROM sys.master_files
WHERE master_files.database_id = db_id()
  AND (master_files.physical_name LIKE '%.MDF' OR master_files.physical_name LIKE '%.LDF')
ORDER BY master_files.name

OPEN Record_cursor

FETCH NEXT FROM Record_cursor
INTO     @name
        ,@physical_name

WHILE (@@FETCH_STATUS = 0)
BEGIN
        -- Process Record
        PRINT 'Shrink ' + @physical_name
        DBCC SHRINKFILE (@name, 0)

        FETCH NEXT FROM Record_cursor
        INTO     @name
                ,@physical_name
END
CLOSE Record_cursor
DEALLOCATE Record_cursor
GO
