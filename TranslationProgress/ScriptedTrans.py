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
        
        # Automatic operations
        if CurrentTag.startswith("parents:") :
            sBaseTag = CurrentTag.removeprefix("parents:")
            if "ship:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["ship:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"亲代：{CurrentSource.removeprefix('cp:')}")
                #Next
                nProcessed += 1
            else :
                nSkipped += 1
            #End If
        elif CurrentTag.startswith("parent:oc:") :
            sBaseTag = CurrentTag.removeprefix("parent:oc:")
            if "oc:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["oc:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"亲代：{CurrentSource.removeprefix('oc:')}")
                #Next
                nProcessed += 1
            else :
                dctTarget[CurrentTag]["TransCn"] = [f"亲代：{sBaseTag}（OC）"]
                nProcessed += 1
            #End If
        elif CurrentTag.startswith("parent:") :
            sBaseTag = CurrentTag.removeprefix("parent:")
            if sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans[sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"亲代：{CurrentSource}")
                #Next
                nProcessed += 1
            else :
                nSkipped += 1
            #End If
        elif CurrentTag.startswith("implied oc:") :
            sBaseTag = CurrentTag.removeprefix("implied oc:")
            if "oc:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["oc:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"暗示{CurrentSource.removeprefix('oc:')}")
                #Next
                nProcessed += 1
            else :
                dctTarget[CurrentTag]["TransCn"] = [f"暗示{sBaseTag}（OC）"]
                nProcessed += 1
            #End If
        elif CurrentTag.startswith("implied ") :
            sBaseTag = CurrentTag.removeprefix("implied ")
            if sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans[sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"暗示{CurrentSource}")
                #Next
                nProcessed += 1
            elif "oc:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["oc:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"暗示{CurrentSource.removeprefix('oc:')}")
                #Next
                nProcessed += 1
            elif "ship:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["ship:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"暗示{CurrentSource.removeprefix('cp:')}")
                #Next
                nProcessed += 1
            else :
                nSkipped += 1
            #End If
        elif CurrentTag.startswith("fusion:oc:") :
            sBaseTag = CurrentTag.removeprefix("fusion:oc:")
            if "oc:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["oc:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"融合：{CurrentSource.removeprefix('oc:')}")
                #Next
                nProcessed += 1
            else :
                dctTarget[CurrentTag]["TransCn"] = [f"融合：{sBaseTag}（OC）"]
                nProcessed += 1
            #End If
        elif CurrentTag.startswith("fusion:") :
            sBaseTag = CurrentTag.removeprefix("fusion:")
            if sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans[sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"融合：{CurrentSource}")
                #Next
                nProcessed += 1
            elif "ship:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["ship:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"融合：{CurrentSource.removeprefix('cp:')}")
                #Next
                nProcessed += 1
            else :
                dctTarget[CurrentTag]["TransCn"] = [f"融合：{sBaseTag}"]
                nProcessed += 1
            #End If
        elif CurrentTag.startswith("futa oc:") :
            sBaseTag = CurrentTag.removeprefix("futa oc:")
            if "oc:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["oc:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"扶她{CurrentSource.removeprefix('oc:')}")
                #Next
                nProcessed += 1
            else :
                dctTarget[CurrentTag]["TransCn"] = [f"扶她{sBaseTag}（OC）"]
                nProcessed += 1
            #End If
        elif CurrentTag.startswith("futa ") :
            sBaseTag = CurrentTag.removeprefix("futa ")
            if sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans[sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"扶她{CurrentSource}")
                #Next
                nProcessed += 1
            elif "oc:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["oc:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"扶她{CurrentSource.removeprefix('oc:')}")
                #Next
                nProcessed += 1
            else :
                dctTarget[CurrentTag]["TransCn"] = [f"扶她{sBaseTag}"]
                nProcessed += 1
            #End If
        elif CurrentTag.startswith("stupid sexy ") :
            sBaseTag = CurrentTag.removeprefix("stupid sexy ")
            if sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans[sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"性感蠢萌{CurrentSource}")
                #Next
                nProcessed += 1
            elif "oc:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["oc:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"性感蠢萌{CurrentSource.removeprefix('oc:')}")
                #Next
                nProcessed += 1
            else :
                dctTarget[CurrentTag]["TransCn"] = [f"性感蠢萌{sBaseTag}"]
                nProcessed += 1
            #End If
        else :
            nSkipped += 1
        #End If
        
        #dctTarget[CurrentTag]["Desc"] = ""
        nTotal += 1
    #Next
    print(f"Total: {nTotal}, Processed: {nProcessed}, Skipped: {nSkipped}")
    
    # Outputting
    Trans.ExportTranslatedTags(dctTarget, sProcessedFile)
#End If