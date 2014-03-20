/**************************************************
File: 03_AddUsersRolesGroups.sql

Description: Setup standard security settings

NOTE: UTL_AddUserToRole_sp will add Users, Roles and login if required.

History:
2014-01-02 Trevor      Created
*************************************************/
PRINT 'Calls to UTL_AddUserToRole_sp'

GO

PRINT 'Database Users and role'
SELECT Username=sysusers.name, Role=Role.name
FROM sysusers
JOIN sysusers Role
  ON Role.uid=sysusers.gid
WHERE sysusers.islogin = 1
GO
