IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.WRK_Data_UPDATE_P_DataID_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.WRK_Data_UPDATE_P_DataID_sp
GO

/**************************************************
File: WRK_Data_UPDATE_P_DataID_sp.sql

Description: Update [WRK_Data].[P_DataID]

History:
2014-01-03    Create  Created
**************************************************/
CREATE PROCEDURE dbo.WRK_Data_UPDATE_P_DataID_sp
AS
SET NOCOUNT ON

SELECT
 [RAW_Data].[CustomerID]
,MAX([RAW_Data].[ShoppingPt]) AS [PurchasePt]
INTO #CustomerPurchasePt
FROM [dbo].[RAW_Data]
WHERE [RAW_Data].[RecordType] = 1 -- Purchase
GROUP BY [RAW_Data].[CustomerID], [RAW_Data].[ShoppingPt]
ORDER BY [RAW_Data].[CustomerID]

UPDATE [WRK_Data] SET
P_DataID = P.[DataID]
FROM [dbo].[WRK_Data]
JOIN [dbo].[RAW_Data] S
  ON S.[DataID] = [WRK_Data].[DataID]
JOIN #CustomerPurchasePt
  ON #CustomerPurchasePt.[CustomerID] = S.[CustomerID]
JOIN [dbo].[RAW_Data] P
  ON P.[CustomerID] = #CustomerPurchasePt.[CustomerID]
 AND P.[ShoppingPt] = #CustomerPurchasePt.[PurchasePt]

DROP TABLE #CustomerPurchasePt
GO

GRANT EXEC, VIEW DEFINITION ON dbo.WRK_Data_UPDATE_P_DataID_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.WRK_Data_UPDATE_P_DataID_sp
*****************************************************/

