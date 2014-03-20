/**************************************************
File: 04_AddLinkedServers.sql

Description: Add Linked Server to SSAS Database

History:
2014-01-08 Trevor      Created
*************************************************/
PRINT 'Add SSAS Linked Server'
--EXEC sp_addlinkedserver @server='My SSAS Server', @provider='MSOLAP', @datasrc='localhost', @catalog='[TITANIC SSAS]';

PRINT 'Add SSAS Linked Server - Access RemoteUser=Trevor-PC\Trevor Password=a'
--EXEC sp_addlinkedsrvlogin @rmtsrvname=N'My SSAS Server',@useself=N'False',@locallogin=NULL,@rmtuser=N'Trevor-PC\Trevor',@rmtpassword='a'
GO
