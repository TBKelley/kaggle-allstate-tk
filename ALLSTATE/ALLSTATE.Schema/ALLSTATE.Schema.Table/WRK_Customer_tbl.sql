IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.WRK_Customer') AND OBJECTPROPERTY(id, 'IsUserTable') = 1))
    DROP TABLE dbo.WRK_Customer
GO

/**************************************************
File: WRK_Customer_tbl.sql

Description: Customer Table
    
History:
2014-03-25    Create  Created
**************************************************/
CREATE TABLE dbo.WRK_Customer 
(
     [CustomerID] INT NOT NULL                  -- Foreign key to RAW_Data
    ,[LastShoppingPt] INT NOT NULL DEFAULT 0    -- Last ShoppingPt in Customer history, where [RecordType]=0
    ,[First_DataID] INT NOT NULL                -- foreign key to RAW_Data for the first ShoppingPt
    ,[Last_DataID] INT NOT NULL                 -- foreign key to RAW_Data for the last ShoppingPt (Not PurchasePt)
    ,[Purchase_DataID] INT NULL                 -- Optional foreign key to RAW_Data for the PurchasePt
    ,[Max_DataID] INT NOT NULL                  -- foreign key to RAW_Data for the last ShoppingPt/PurchasePt
)
GO

ALTER TABLE dbo.WRK_Customer
ADD CONSTRAINT WRK_Customer_PK
PRIMARY KEY NONCLUSTERED ([CustomerID])
GO

-- Logical Business Key
-- DROP INDEX dbo.WRK_Customer.WRK_Customer_BK
CREATE UNIQUE CLUSTERED INDEX WRK_Customer_BK
ON dbo.WRK_Customer([CustomerID])
WITH FILLFACTOR = 90;
GO

GRANT DELETE, INSERT, REFERENCES, SELECT, UPDATE, VIEW DEFINITION ON dbo.WRK_Customer TO PUBLIC
GO
