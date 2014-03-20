IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.RAW_Data_UPDATE_DataType_Validation_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.RAW_Data_UPDATE_DataType_Validation_sp
GO

/**************************************************
File: RAW_Data_UPDATE_DataType_Validation_sp.sql

Description: Reset the DataType=2 for 10% of data as validation data.

History:
2014-01-03    Create  Created
**************************************************/
CREATE PROCEDURE dbo.RAW_Data_UPDATE_DataType_Validation_sp
   @Seed INT = 0
  ,@ValidationPct FLOAT = 0.1
AS
SET NOCOUNT ON -- Required for VBA

DECLARE @Random FLOAT
SET @Random =  RAND(@Seed)

-- This SQL code uses a CURSOR technique to iterate through a resultset
SET NOCOUNT ON

-- Source table fields
DECLARE  @DataID  INT

DECLARE Record_cursor CURSOR FORWARD_ONLY READ_ONLY FOR
SELECT [DataID]
FROM [dbo].[RAW_Data]
WHERE [DataType] IN (1, 2) -- Training data = Train + Cross Validation
ORDER BY [DataID]

OPEN Record_cursor

FETCH NEXT FROM Record_cursor
INTO @DataID

WHILE (@@FETCH_STATUS = 0)
BEGIN
    SET @Random = RAND()
    IF (@Random < @ValidationPct)
     BEGIN
--PRINT '@Random=' + CAST(@Random AS VARCHAR(20)) + ' @ValidationPct=' + CAST(@ValidationPct AS VARCHAR(20))
        UPDATE [dbo].[RAW_Data] SET
        [DataType] = 2 -- Validation
        WHERE [DataID] = @DataID
     END
    ELSE
     BEGIN
        UPDATE [dbo].[RAW_Data] SET
        [DataType] = 1 -- Training
        WHERE [DataID] = @DataID
     END
      
    FETCH NEXT FROM Record_cursor
    INTO @DataID
END
CLOSE Record_cursor
DEALLOCATE Record_cursor

GO

GRANT EXEC, VIEW DEFINITION ON dbo.RAW_Data_UPDATE_DataType_Validation_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.RAW_Data_UPDATE_DataType_Validation_sp
DECLARE @CountTotal INT
DECLARE @CountValidation INT
DECLARE @ValidationPct FLOAT
SELECT @CountTotal=COUNT(*) FROM [dbo].[RAW_Data] WHERE [DataType] IN (1, 2)
SELECT @CountValidation=COUNT(*) FROM [dbo].[RAW_Data] WHERE [DataType] IN (2)
SET @ValidationPct = @CountValidation * 1.0 / (@CountTotal * 1.0)
PRINT 'Total training records     = ' + CAST(@CountTotal AS VARCHAR(20))
PRINT 'Total Validation records   = ' + CAST(@CountValidation AS VARCHAR(20)) + ' ' + CAST(@ValidationPct AS VARCHAR(20))
*****************************************************/

