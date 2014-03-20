IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.RAW_Data_FAILED_vw') AND OBJECTPROPERTY(id, 'IsView') = 1))
    DROP VIEW dbo.RAW_Data_FAILED_vw
GO

/**************************************************
File: RAW_Data_FAILED_vw.sql

Description: DataID of all Traning Data that predicted incorrectly
    
History:
2014-01-03    Create  Created
**************************************************/
CREATE VIEW dbo.RAW_Data_FAILED_vw AS
SELECT
 [RAW_Data].[DataID]
FROM [dbo].[RAW_Data]
JOIN [dbo].[DRV_Predict]
  ON [DRV_Predict].[DataID] = [RAW_Data].[DataID]
 AND [DRV_Predict].[Model] = 'Ensumble1'
WHERE [DataType] = 1
  AND ([RAW_Data].[Actual] <> [DRV_Predict].[Predicted])

GO

GRANT SELECT, VIEW DEFINITION ON dbo.RAW_Data_FAILED_vw TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT * FROM dbo.RAW_Data_FAILED_vw
*****************************************************/
