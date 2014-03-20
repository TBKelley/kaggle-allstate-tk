IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.DRV_Predict_vw') AND OBJECTPROPERTY(id, 'IsView') = 1))
    DROP VIEW dbo.DRV_Predict_vw
GO

/**************************************************
File: DRV_Predict_vw.sql

Description: Predition Results

History:
2014-01-03    Create  Created
**************************************************/
CREATE VIEW [dbo].[DRV_Predict_vw] AS

SELECT
 [DRV_Predict].[Model]
,[RAW_Data].[PassengerId]
,[DRV_Predict].[Predicted]
,[DRV_Predict].[Probablity]
,[RAW_Data].[DataType]
FROM [dbo].[DRV_Predict]
JOIN [dbo].[RAW_Data]
  ON [RAW_Data].[DataID] = [DRV_Predict].[DataID]

GO

GRANT SELECT, VIEW DEFINITION ON dbo.DRV_Predict_vw TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT * FROM [dbo].[DRV_Predict_vw]
SELECT * FROM [dbo].[DRV_Predict_vw] WHERE [Model]='Perceptron'
*****************************************************/
