IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.WRK_Data_INSERT_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.WRK_Data_INSERT_sp
GO

/**************************************************
File: WRK_Data_INSERT_sp.sql

Description: INSERT [dbo].[WRK_Data] with default values.

History:
2014-01-24    Create  Created
**************************************************/
CREATE PROCEDURE dbo.WRK_Data_INSERT_sp
AS
SET NOCOUNT ON

INSERT [WRK_Data] ([DataID])
SELECT [RAW_Data].[DataID]
FROM [dbo].[RAW_Data]

GO

GRANT EXEC, VIEW DEFINITION ON dbo.WRK_Data_INSERT_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.WRK_Data_INSERT_sp
*****************************************************/

