IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.WRK_Train_OnlyLastShoppingPt_vw') AND OBJECTPROPERTY(id, 'IsView') = 1))
    DROP VIEW dbo.WRK_Train_OnlyLastShoppingPt_vw
GO

/**************************************************
File: WRK_Train_OnlyLastShoppingPt_vw.sql

Description: Used for training alorithm that predict PurchasePt Optiosn from Customer Properties.
             We only care about the final training PurchasePt or final test ShoppingPt.

History:
2014-03-26  Create      Created
**************************************************/
CREATE VIEW [dbo].[WRK_Train_OnlyLastShoppingPt_vw] AS

SELECT
 [RAW_Data].[DataID]
,[RAW_Data].[DataType]
,[RAW_Data].[CustomerId]
-- Y Classes
,[RAW_Data].[A] AS [P_A]                               -- 0,1,2
,[RAW_Data].[B] AS [P_B]                               -- 0,1
,[RAW_Data].[C] AS [P_C]                               -- 1,2,3,4
,[RAW_Data].[D] AS [P_D]                               -- 1,2,3
,[RAW_Data].[E] AS [P_E]                               -- 0,1
,[RAW_Data].[F] AS [P_F]                               -- 0,1,2,3
,[RAW_Data].[G] AS [P_G]                               -- 1,2,3,4

-- X Features
,[RAW_Data].[State] -- "AL", …"WY"
,ISNULL([RAW_Data].[Location],0) AS [Location]         -- 10001,10002,…16580,0
,[RAW_Data].[GroupSize]                                -- 1,2,3,4
,CAST([RAW_Data].[HomeOwner] AS INT) AS [HomeOwner]    -- 0,1
,[RAW_Data].[CarAge]                                   -- 0,1,2,…85
,ISNULL([RAW_Data].[CarValue], 'z') AS [CarValue]      -- "a","b",…"i",NA='z'
,ISNULL([RAW_Data].[RiskFactor], 0) AS [RiskFactor]    -- 1,2,3,4,NA=0
,[RAW_Data].[AgeOldest]                                -- 18,19,…75
,[RAW_Data].[AgeYoungest]                              -- 16,17,…75
,CAST([RAW_Data].[MarriedCouple] AS INT) AS [MarriedCouple] -- 0,1
,ISNULL([RAW_Data].[CPrevious], 0) AS   [CPrevious]    -- 1,2,3,4,NA=0
,ISNULL([RAW_Data].[DurationPrevious],16) AS [DurationPrevious] -- 0,1,2,…15,NA=16
,[RAW_Data].[Cost]                                     -- 260..922
FROM [dbo].[RAW_Data]
JOIN [dbo].[WRK_Data]
  ON [WRK_Data].[DataID] = [RAW_Data].[DataID]
JOIN [dbo].[WRK_Customer]
  ON [WRK_Customer].[Max_DataID] = [RAW_Data].[DataID]
--WHERE [RAW_Data].[DataType] IN (1, 2, 3, 9) -- Selection done in .py

GO

GRANT SELECT, VIEW DEFINITION ON dbo.WRK_Train_OnlyLastShoppingPt_vw TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT * FROM [dbo].[WRK_Train_OnlyLastShoppingPt_vw] WHERE [DataType] IN (1,2) ORDER BY [DataID] -- Training+Cross
SELECT * FROM [dbo].[WRK_Train_OnlyLastShoppingPt_vw] WHERE [DataType] IN (3) ORDER BY [DataID]  -- Test
*****************************************************/
