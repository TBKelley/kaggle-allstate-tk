IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.RAW_Errors_vw') AND OBJECTPROPERTY(id, 'IsView') = 1))
    DROP VIEW dbo.RAW_Errors_vw
GO

/**************************************************
File: RAW_Errors_vw.sql

Description: RAW_Data view of Training data not correctly predicted.
    
History:
2014-01-03    Create  Created
**************************************************/
CREATE VIEW dbo.RAW_Errors_vw AS
SELECT [DRV_Predict].[DataID]
FROM [dbo].[DRV_Predict]
JOIN [dbo].[RAW_Data]
  ON [RAW_Data].[DataID] = [DRV_Predict].[DataID]
WHERE [DRV_Predict].[Model] = 'Ensumble1'
  AND [RAW_Data].[Actual] <> [DRV_Predict].[Predicted]

GO

GRANT SELECT, VIEW DEFINITION ON dbo.RAW_Errors_vw TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT * FROM dbo.RAW_Errors_vw
*****************************************************/
