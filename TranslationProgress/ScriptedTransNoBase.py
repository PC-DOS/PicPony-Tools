import os
import copy
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

# Intersect arrays (get intersection)
# Duplicate elements will be merged
# If sEmptyListOperation is set to "none", will do normal mathematical intersection calculation (Set1 & EmptySet == EmptySet)
# If sEmptyListOperation is set to "keep" and one of the given arrays is empty, intersection will not be calculated, and will return another array (Set1 & EmptySet == Set1)
def IntersectArrays(arrArray1 : list, arrArray2 : list,
    IsDuplicateItemsDropped : bool = True, sEmptyListOperation : str = "none") -> list :

    # Check if one of the given arrays is empty
    if sEmptyListOperation.lower() == "keep" :
        if len(arrArray1) == 0 :
            return copy.deepcopy(arrArray2)
        elif len(arrArray2) == 0 :
            return copy.deepcopy(arrArray1)
        #End If
    #End If

    arrResult = []
    for CurrentElement in arrArray1 :
        if (CurrentElement in arrResult) and IsDuplicateItemsDropped :
            continue
        #End If
        if CurrentElement in arrArray2 :
            if (CurrentElement in arrResult) and IsDuplicateItemsDropped :
                continue
            #End If
            arrResult.append(CurrentElement)
        #End If
    #Next

    return arrResult
#End Function

# Join multiple string arrays
# For example, arrStrArray=[["a1","a2"], ["b1","b2"]], sSeparator=" x "
# This func will return ["a1 x b1", "a1 x b2", "a2 x b1", "a2 x b2"]
def JoinMultipleStringArray(arrStrArray : list, sSeparator : str) -> list :
    arrResult = []
    
    if len(arrStrArray) == 1 :
        arrResult = [str(obj) for obj in arrStrArray[0]]
    else :
        arrNestedResult = JoinMultipleStringArray(arrStrArray[1:], sSeparator)
        for str1 in arrStrArray[0] :
            for str2 in arrNestedResult :
                arrResult.append(str(str1) + sSeparator + str2)
            #Next
        #Next
    #End If
    
    return arrResult
#End Function

if __name__ == "__main__" :
    # Load translations
    sTransFile = "tags_translated_1786981181742.jsonl"
    dctTrans = Trans.LoadTranslatedTags(sTransFile)
    sTransTimestamp = pathlib.Path(sTransFile).stem
    sTransTimestamp = sTransTimestamp.removeprefix("tags_translated_")
    dUnixTimestampMs = int(sTransTimestamp)
    dtmTransTimestamp = datetime.datetime.fromtimestamp(dUnixTimestampMs / 1000.0)
    sTransTimestamp = dtmTransTimestamp.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Translation file timestamp: {sTransTimestamp}")
    
    # Load source trans
    sTragetFile = "Job:Rule63_OC"
    sProcessedFile = "tags_trans_output.jsonl"
    dctTarget = dict()
    
    # Load Derpibooru database dump
    IsDerpibooruDbNeeded = True
    if IsDerpibooruDbNeeded :
        dbDerpibooru = DerpibooruDatabaseDump("derpibooru_public_dump_2026_08_15.pgdump")
        dbDerpibooru.PrintInfo()
        sDerpibooruTimestamp = dbDerpibooru.GetTimestamp()
        print("Getting tags ...")
        dctTagsByName = dbDerpibooru.GetTagsByName()
        dctTagsById = dbDerpibooru.GetTagsById()
        nTags = len(dctTagsById.keys())
        print(f"{nTags} tags found in database dump")
        print("Getting image tags ...")
        if os.path.exists("_Cache/dctImageTags.pkl") :
            with open("_Cache/dctImageTags.pkl", "rb") as filObjDump : 
                dctImageTags = pickle.load(filObjDump)
            #End With
        else :
            dctImageTags = dbDerpibooru.GetImageTags()
            with open("_Cache/dctImageTags.pkl", "wb") as filObjDump : 
                pickle.dump(dctImageTags, filObjDump)
            #End With
        #End If
        nImages = len(dctImageTags.keys())
        print(f"{nImages} images found in database dump")
        print("Getting hidden images ...")
        dctImageHides = dbDerpibooru.GetImageHides()
        nImageHides = len(dctImageHides.keys())
        print(f"{nImageHides} image hides found in database dump")
        print("Getting tag implications ...")
        dctTagImpl = dbDerpibooru.GetTagImplications()
        nTagImpl = len(dctTagImpl.keys())
        print(f"{nTagImpl} tag implications found in database dump")
    #End If
    
    # Batch translating
    nTotal = 0
    nProcessed = 0
    nSkipped = 0
    if sTragetFile.lower() == "Job:Rule63".lower() :
        iRule63TagId = dctTagsByName["rule 63"]["Id"]
        for CurrentTagId in dctTagImpl.keys() :
            sCurrentTag = dctTagsById[CurrentTagId]["Name"]
            if sCurrentTag in dctTrans.keys() :
                continue
            #End If
            
            arrCurrentImpl = dctTagImpl[CurrentTagId]
            
            if iRule63TagId in arrCurrentImpl :
                nCharacterCount = 0
                for SubTagId in arrCurrentImpl :
                    if (not (dctTagsById[SubTagId]["Category"] is None)) and (dctTagsById[SubTagId]["Category"].lower() == "character") :
                        nCharacterCount += 1
                    #End If
                #Next
                if nCharacterCount != 1 :
                    continue
                #End If
            
                for SubTagId in arrCurrentImpl :
                    if SubTagId != iRule63TagId :
                        if (not (dctTagsById[SubTagId]["Category"] is None)) and (dctTagsById[SubTagId]["Category"].lower() == "character") :
                            sCurrentBaseTag = dctTagsById[SubTagId]["Name"]
                            print(f"Hit tag: {sCurrentTag}, base tag: {sCurrentBaseTag}")
                            dctCurrentTag = dict(TransCn=[], Desc="")
                            if sCurrentBaseTag in dctTrans.keys() :
                                for CurrentTrans in dctTrans[sCurrentBaseTag]["TransCn"] :
                                    dctCurrentTag["TransCn"].append(f"性转{CurrentTrans}")
                                #Next
                            else :
                                dctCurrentTag["TransCn"].append(f"性转{sCurrentBaseTag}")
                            #End If
                            dctTarget[sCurrentTag] = dctCurrentTag
                            nProcessed += 1
                            nTotal += 1
                            break
                        #End If
                    #End If
                #Next
            #End If
        #Next
    #End If
    print(f"Total: {nTotal}, Processed: {nProcessed}, Skipped: {nSkipped}")
    
    # Outputting
    Trans.ExportTranslatedTags(dctTarget, sProcessedFile)
#End If