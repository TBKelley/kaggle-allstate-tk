IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.DRV_Predict_LOAD_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.DRV_Predict_LOAD_sp
GO

/**************************************************
File: DRV_Predict_LOAD_sp.sql

Description: Predition Results

Parameters:
@Model   : Predictive Model

History:
2014-01-03    Create  Created
**************************************************/
CREATE PROCEDURE dbo.DRV_Predict_LOAD_sp
   @Model     VARCHAR(50) = 'RandomForest'
AS
SET NOCOUNT ON -- Required for VBA

SELECT
 [Model]
,[PassengerId]
,[Predicted]
,[Probablity]
FROM [dbo].[DRV_Predict_vw]
WHERE [Model] = @Model
  AND [DataType] = 3 -- Test
ORDER BY [Model], [PassengerId]

GO

GRANT EXEC, VIEW DEFINITION ON dbo.DRV_Predict_LOAD_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.DRV_Predict_LOAD_sp @Model='RandomForest'
EXEC dbo.DRV_Predict_LOAD_sp @Model='Perceptron'
*****************************************************/

