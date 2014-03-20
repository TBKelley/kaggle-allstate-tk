IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.WRK_Data_UPDATE_CrossRow_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.WRK_Data_UPDATE_CrossRow_sp
GO

/**************************************************
File: WRK_Data_UPDATE_CrossRow_sp.sql

Description: Update features that cross rows [Xxxxx],[Xxxxx].

History:
2014-01-03    Create  Created
**************************************************/
CREATE PROCEDURE dbo.WRK_Data_UPDATE_CrossRow_sp
AS
SET NOCOUNT ON -- Required for VBA

GO

GRANT EXEC, VIEW DEFINITION ON dbo.WRK_Data_UPDATE_CrossRow_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.WRK_Data_UPDATE_CrossRow_sp
*****************************************************/

