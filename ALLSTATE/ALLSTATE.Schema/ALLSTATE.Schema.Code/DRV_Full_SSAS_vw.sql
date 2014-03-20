IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.DRV_Full_SSAS_vw') AND OBJECTPROPERTY(id, 'IsView') = 1))
    DROP VIEW dbo.DRV_Full_SSAS_vw
GO

/**************************************************
File: DRV_Full_SSAS_vw.sql

Description: SSAS Prediction features

History:
2014-01-03    Create  Created
**************************************************/
CREATE VIEW [dbo].[DRV_Full_SSAS_vw] AS

SELECT
 [RAW_Data].[DataID]
,[RAW_Data].[DataType]
,[RAW_Data].[Actual]
,[RAW_Data].[Pclass]
,[WRK_Data].[SexINT]
,[WRK_Data].[SalutationHash]
,[WRK_Data].[EmbarkedINT]
,[WRK_Data].[AgeFLOAT]
,[WRK_Data].[FareFLOAT]
,dbo.SafeLOG10_fn([WRK_Data].[FareFLOAT]) AS [FareLOG10]
,[WRK_Data].[IsChild]
,[WRK_Data].[IsAdult]
,[WRK_Data].[HasFamily]
,[WRK_Data].[HasParent]
,[WRK_Data].[HasChild]
,[WRK_Data].[HasSpouse]
,[WRK_Data].[HasSibling]
,[WRK_Data].[Parents]
,[WRK_Data].[Children]
,[WRK_Data].[Sibling]
,[WRK_Data].[DeptCodeHash]
,[WRK_Data].[DeckHash]
,[WRK_Data].[DualOccupant]
,[WRK_Data].[OtherSurvivers]
,[WRK_Data].[HasOtherSurviver]
,[WRK_Data].[OtherDied]
,[WRK_Data].[HasOtherDied]
FROM [dbo].[WRK_Data]
JOIN [dbo].[RAW_Data]
  ON [RAW_Data].[DataID] = [WRK_Data].[DataID]
-- AND [RAW_Data].[DataType] IN (1, 2, 3, 9)

GO

GRANT SELECT, VIEW DEFINITION ON dbo.DRV_Full_SSAS_vw TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT * FROM [dbo].[DRV_Full_SSAS_vw]
*****************************************************/
