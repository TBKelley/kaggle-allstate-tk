@ECHO ON
SET Model=DTree
SET AscmdUNC=C:\Program Files\Microsoft SQL Server\110\Samples\Analysis Services\Administrator\ascmd\Ascmd.exe
CHDIR /D "D:\DEV_2012\Kaggle\TitanicLoad.root\TitanicLoad\XMLA"

REM No -U Username -P Password is required as SSAS database has "Security\RequireClientAuthentication" = false.
"%AscmdUNC%" -S Trevor-PC -d "TITANIC SSAS" -i "Model_PROCESS.xmla" -o "%Model%_PROCESS.xml" -v model=%Model%
IF ERRORLEVEL 1 GOTO :ERROR_RETURN

@ECHO -----------------------------------------------------------------
@ECHO SUCESSFULLY COMPLETED Process "%Model%"
@ECHO =================================================================
EXIT /B 0
REM ------ Main End ------------------------------------

REM Return error message
:ERROR_RETURN
@ECHO .
@ECHO -----------------------------------------------------------------
@ECHO UNEXPECTED ERROR STOPPED Process "%Model%"
@ECHO =================================================================
EXIT /B 1
