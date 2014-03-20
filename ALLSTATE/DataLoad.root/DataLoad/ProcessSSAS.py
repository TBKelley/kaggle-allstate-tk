#!/usr/bin/python
from subprocess import call
import SharedLibrary
import Context
import os

def Execute(context):
    
    ProcessModel(context.SsasInstance, "DTree")
    ProcessModel(context.SsasInstance, "LogisticR")
    ProcessModel(context.SsasInstance, "NBays")
    ProcessModel(context.SsasInstance, "NNetwork")

def ProcessModel(ssasInstance, model):
    AscmdUNC = "C:/Program Files/Microsoft SQL Server/110/Samples/Analysis Services/Administrator/ascmd/Ascmd.exe"
    try:
        cwd = os.getcwd()
        return_code = call([AscmdUNC, '-S', ssasInstance, '-d', 'TITANIC SSAS', '-i', 'XMLA\\Model_PROCESS.xmla', '-o', 'XMLA\\' + model + '_PROCESS.xml', '-v', 'model=' + model])
        if (return_code != 0):
            raise Exception("Error processing model=" + model)
    except:
        import traceback
        traceback.print_exc()
        raise Exception("Error processing model=" + model + " ABORT")

