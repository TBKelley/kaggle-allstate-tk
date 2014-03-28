IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.WRK_Train_Base_vw') AND OBJECTPROPERTY(id, 'IsView') = 1))
    DROP VIEW dbo.WRK_Train_Base_vw
GO

/**************************************************
File: WRK_Train_Base_vw.sql

Description: Used for training Base alorithm

History:
2014-01-03    Create  Created
**************************************************/
CREATE VIEW [dbo].[WRK_Train_Base_vw] AS

SELECT
 [RAW_Data].[DataID]
,[RAW_Data].[DataType]
,[RAW_Data].[CustomerId]
-- Y Classes
,P.[A] AS [P_A]                               -- 0,1,2
,P.[B] AS [P_B]                               -- 0,1
,P.[C] AS [P_C]                               -- 1,2,3,4
,P.[D] AS [P_D]                               -- 1,2,3
,P.[E] AS [P_E]                               -- 0,1
,P.[F] AS [P_F]                               -- 0,1,2,3
,P.[G] AS [P_G]                               -- 1,2,3,4

,[RAW_Data].[A]                                        -- 0,1,2
,[RAW_Data].[B]                                        -- 0,1
,[RAW_Data].[C]                                        -- 1,2,3,4
,[RAW_Data].[D]                                        -- 1,2,3
,[RAW_Data].[E]                                        -- 0,1
,[RAW_Data].[F]                                        -- 0,1,2,3
,[RAW_Data].[G]                                        -- 1,2,3,4
FROM [dbo].[RAW_Data]
JOIN [dbo].[WRK_Data]
  ON [WRK_Data].[DataID] = [RAW_Data].[DataID]
LEFT JOIN [dbo].[RAW_Data] P
  ON P.[DataID] = [WRK_Data].[P_DataID]
JOIN [dbo].[WRK_Customer]
  ON [WRK_Customer].[CustomerID] = [RAW_Data].[CustomerId]
 AND [WRK_Customer].[Last_DataID] = [RAW_Data].[DataID]
WHERE [RAW_Data].[RecordType] <> 1 -- Exclude PurchasePt else we would be predicting PurchasePt from PurchasePt
--WHERE [RAW_Data].[DataType] IN (1, 2, 3, 9) -- Selection done in .py

GO

GRANT SELECT, VIEW DEFINITION ON dbo.WRK_Train_Base_vw TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT * FROM [dbo].[WRK_Train_Base_vw] WHERE [DataType] IN (1,2) -- Training+Cross
SELECT * FROM [dbo].[WRK_Train_Base_vw] WHERE [DataType] IN (3)   -- Test
*****************************************************/
