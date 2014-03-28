IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.RAW_Data') AND OBJECTPROPERTY(id, 'IsUserTable') = 1))
    DROP TABLE dbo.RAW_Data
GO

/**************************************************
File: RAW_Data_tbl.sql

Description: Kaggle "Allstate Purchase Prediction Challenge" raw Dataing/Data data

SIZE: 665,249 Shopping Pt, 97,009 Customers, 

History:
2014-03-14    Create  Created
**************************************************/
CREATE TABLE dbo.RAW_Data 
(
     [DataID]  INT IDENTITY(10,1) NOT NULL      -- Set SEED>1 if predefined records
    ,[DataType] TINYINT NOT NULL DEFAULT 1      -- 1=Training, 2=Cross Validation, 3=Test, 9=Boosted replica
    ,[CustomerId] INT NOT NULL                  -- 97,009 Customers. Example: 10000001
    ,[ShoppingPt] SMALLINT NOT NULL             -- 1,2,…13 
    ,[RecordType] TINYINT NOT NULL              -- 0,1
    ,[Day] TINYINT NOT NULL                     -- 0=MON,…5=SAT,6=SUN, Day of Week
    ,[Time] DATETIME NOT NULL                   -- 00:01…23:59
    ,[State] CHAR(2) NOT NULL                   -- "AL", …"WY"
    ,[Location] INT NULL                        -- 10001,10002,…16580,NA
    ,[GroupSize] TINYINT NOT NULL               -- 1,2,3,4
    ,[HomeOwner] BIT NOT NULL                   -- 0,1
    ,[CarAge] TINYINT NOT NULL                  -- 0,1,2,…85
    ,[CarValue] CHAR(1) NULL                    -- "a","b",…"i",NA
    ,[RiskFactor] TINYINT NULL                  -- 1,2,3,4,NA
    ,[AgeOldest] TINYINT NOT NULL               -- 18,19,…75
    ,[AgeYoungest] TINYINT NOT NULL             -- 16,17,…75
    ,[MarriedCouple] BIT NOT NULL               -- 0,1
    ,[CPrevious] TINYINT NULL                   -- 1,2,3,4,NA
    ,[DurationPrevious] TINYINT NULL            -- 0,1,2,…15,NA
    ,[A] TINYINT NOT NULL                       -- 0,1,2
    ,[B] TINYINT NOT NULL                       -- 0,1
    ,[C] TINYINT NOT NULL                       -- 1,2,3,4
    ,[D] TINYINT NOT NULL                       -- 1,2,3
    ,[E] TINYINT NOT NULL                       -- 0,1
    ,[F] TINYINT NOT NULL                       -- 0,1,2,3
    ,[G] TINYINT NOT NULL                       -- 1,2,3,4
    ,[Cost] SMALLINT NOT NULL                   -- 260..922
)
GO

ALTER TABLE dbo.RAW_Data
ADD CONSTRAINT RAW_Data_PK
PRIMARY KEY NONCLUSTERED (DataID)
GO

-- Logical Business Key
-- DROP INDEX dbo.RAW_Data.RAW_Data_BK
CREATE CLUSTERED INDEX RAW_Data_BK
ON dbo.RAW_Data(CustomerId, ShoppingPt)
WITH FILLFACTOR = 90;
GO

-- Secondary Index
-- DROP INDEX dbo.RAW_Data_DataType_IDX
CREATE UNIQUE INDEX RAW_Data_DataType_IDX
ON dbo.RAW_Data([DataType], [DataID]);
GO

GRANT DELETE, INSERT, REFERENCES, SELECT, UPDATE, VIEW DEFINITION ON dbo.RAW_Data TO PUBLIC
GO


