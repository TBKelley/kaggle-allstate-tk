IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.DRV_Train_SSAS_vw') AND OBJECTPROPERTY(id, 'IsView') = 1))
    DROP VIEW dbo.DRV_Train_SSAS_vw
GO

/**************************************************
File: DRV_Train_SSAS_vw.sql

Description: SSAS Prediction features

History:
2014-01-03    Create  Created
**************************************************/
CREATE VIEW [dbo].[DRV_Train_SSAS_vw] AS

SELECT *
FROM [dbo].[DRV_Full_SSAS_vw]
WHERE [DataType] IN (1, 9) --  Train, Boost

GO

GRANT SELECT, VIEW DEFINITION ON dbo.DRV_Train_SSAS_vw TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT * FROM [dbo].[DRV_Train_SSAS_vw]
*****************************************************/
