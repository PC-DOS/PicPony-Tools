import os
import pickle
import datetime
import pathlib

import numpy as np
import matplotlib.pyplot as plt

#import TranslatedTagsUtilPlainText as Trans
import TranslatedTagsUtilJSON as Trans
from DerpibooruDatabaseDump import DerpibooruDatabaseDump

# Dump an object to persistent file on disk
def DumpObjectToFile(objInstance : object, sPath : str) :
    import pickle
    with open(sPath, "wb") as filObjDump :
        pickle.dump(objInstance, filObjDump)
    #End With
#End Sub

# Load an object from persistent file on disk
def LoadObjectFromFile(sPath : str) -> object :
    import pickle
    with open(sPath, "rb") as filObjDump :
        objInstance = pickle.load(filObjDump)
    #End With
    return objInstance
#End Function

if __name__ == "__main__" :
    # Load translations
    sTransFile = "tags_translated_1786945553220.jsonl"
    dctTrans = Trans.LoadTranslatedTags(sTransFile)
    sTransTimestamp = pathlib.Path(sTransFile).stem
    sTransTimestamp = sTransTimestamp.removeprefix("tags_translated_")
    dUnixTimestampMs = int(sTransTimestamp)
    dtmTransTimestamp = datetime.datetime.fromtimestamp(dUnixTimestampMs / 1000.0)
    sTransTimestamp = dtmTransTimestamp.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Translation file timestamp: {sTransTimestamp}")
    
    # Load source trans
    sTragetFile = "tags_page_1.jsonl"
    sProcessedFile = "tags_trans_output.jsonl"
    dctTarget = Trans.LoadTranslatedTags(sTragetFile)
    
    # Batch translating
    nTotal = 0
    nProcessed = 0
    nSkipped = 0
    for CurrentTag in dctTarget.keys() :
        sBaseTag = CurrentTag.removeprefix("parent:")
        #if sBaseTag in dctTrans.keys() :
        if True :
            #arrCurrentSource = dctTrans[sBaseTag]["TransCn"]
            dctTarget[CurrentTag]["TransCn"] = [f"亲代：{sBaseTag}"]
            #for CurrentSource in arrCurrentSource :
            #    dctTarget[CurrentTag]["TransCn"].append(f"亲代：{CurrentSource}")
            #Next
            nProcessed += 1
        else :
            nSkipped += 1
        #End If
        nTotal += 1
    #Next
    print(f"Total: {nTotal}, Processed: {nProcessed}, Skipped: {nSkipped}")
    
    # Outputting
    Trans.ExportTranslatedTags(dctTarget, sProcessedFile)
#End If