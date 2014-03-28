IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.WRK_Customer_INSERT_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.WRK_Customer_INSERT_sp
GO

/**************************************************
File: WRK_Customer_INSERT_sp.sql

Description: INSERT [dbo].[WRK_Customer] with default values.

History:
2014-01-24    Create  Created
**************************************************/
CREATE PROCEDURE dbo.WRK_Customer_INSERT_sp
AS
SET NOCOUNT ON

INSERT [dbo].[WRK_Customer] ([CustomerID], [LastShoppingPt], [First_DataID], [Last_DataID], [Max_DataID])
SELECT
 [RAW_Data].[CustomerId] AS [CustomerID]
,MAX([RAW_Data].[ShoppingPt]) AS [LastShoppingPt]
,MIN([RAW_Data].[DataID]) AS [First_DataID]
,MAX([RAW_Data].[DataID]) AS [Last_DataID]
,MAX([RAW_Data].[DataID]) AS [Max_DataID]
FROM [dbo].[RAW_Data]
WHERE [RAW_Data].[RecordType] = 0
GROUP BY [RAW_Data].[CustomerId]

INSERT [dbo].[WRK_Customer] ([CustomerID], [LastShoppingPt], [First_DataID], [Last_DataID], [Max_DataID])
SELECT
 [RAW_Data].[CustomerId] AS [CustomerID]
,0 AS [LastShoppingPt]
,0 AS [First_DataID]
,0 AS [Last_DataID]
,0 AS [Max_DataID]
FROM [dbo].[RAW_Data]
WHERE [RAW_Data].[RecordType] = 1
  AND [RAW_Data].[CustomerId] NOT IN (SELECT E.[CustomerID] FROM [dbo].[WRK_Customer] E)

UPDATE [WRK_Customer] SET
 [Purchase_DataID] = [RAW_Data].[DataID]
,[Max_DataID] = [RAW_Data].[DataID]  -- MAX([Purchase_DataID], [Last_DataID])
FROM [dbo].[WRK_Customer]
JOIN [dbo].[RAW_Data]
  ON [RAW_Data].[CustomerId] = [WRK_Customer].[CustomerID]
 AND [RAW_Data].[RecordType] = 1

GO

GRANT EXEC, VIEW DEFINITION ON dbo.WRK_Customer_INSERT_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
TRUNCATE TABLE dbo.WRK_Customer
EXEC dbo.WRK_Customer_INSERT_sp
*****************************************************/

