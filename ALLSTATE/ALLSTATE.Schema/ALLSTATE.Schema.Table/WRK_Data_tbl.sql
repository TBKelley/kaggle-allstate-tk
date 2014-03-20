IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.WRK_Data') AND OBJECTPROPERTY(id, 'IsUserTable') = 1))
    DROP TABLE dbo.WRK_Data
GO

/**************************************************
File: WRK_Data_tbl.sql

Description: Kaggle "Allstate Purchase Prediction Challenge" raw training data
    
History:
2014-03-14    Create  Created
**************************************************/
CREATE TABLE dbo.WRK_Data 
(
     [DataID]  INT NOT NULL         -- Foreign key to RAW_Data
)
GO

ALTER TABLE dbo.WRK_Data
ADD CONSTRAINT WRK_Data_PK
PRIMARY KEY NONCLUSTERED ([DataID])
GO

-- Logical Business Key
-- DROP INDEX dbo.WRK_Data.WRK_Data_BK
CREATE UNIQUE CLUSTERED INDEX WRK_Data_BK
ON dbo.WRK_Data([DataID])
WITH FILLFACTOR = 90;
GO

GRANT DELETE, INSERT, REFERENCES, SELECT, UPDATE, VIEW DEFINITION ON dbo.WRK_Data TO PUBLIC
GO
