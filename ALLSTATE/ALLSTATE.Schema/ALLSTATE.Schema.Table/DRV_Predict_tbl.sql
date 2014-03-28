IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.DRV_Predict') AND OBJECTPROPERTY(id, 'IsUserTable') = 1))
    DROP TABLE dbo.DRV_Predict
GO

/**************************************************
File: DRV_Predict_tbl.sql

Description: Kaggle "Allstate Purchase Prediction Challenge" raw training data
    
History:
2014-03-14    Create  Created
**************************************************/
CREATE TABLE dbo.DRV_Predict 
(
     [PredictID] INT IDENTITY(10,1) NOT NULL -- Set SEED>1 if predefined records
    ,[Model] VARCHAR(50) NOT NULL   -- Business key, Learning model
    ,[DataID]  INT NOT NULL         -- Business key, Foreign key to RAW_Data.
    ,[Predicted] VARCHAR(7) NOT NULL -- Predicted value. ABCDEFG. Example: '0032003'
    ,[Probablity] FLOAT NOT NULL    -- Probability of [Predicted]=1
)
GO

ALTER TABLE dbo.DRV_Predict
ADD CONSTRAINT DRV_Predict_PK
PRIMARY KEY NONCLUSTERED ([PredictID])
GO

-- Logical Business Key
-- DROP INDEX dbo.DRV_Predict.DRV_Predict_BK
CREATE UNIQUE CLUSTERED INDEX DRV_Predict_BK
ON dbo.DRV_Predict([Model], [DataID])
WITH FILLFACTOR = 90;
GO

GRANT DELETE, INSERT, REFERENCES, SELECT, UPDATE, VIEW DEFINITION ON dbo.DRV_Predict TO PUBLIC
GO
