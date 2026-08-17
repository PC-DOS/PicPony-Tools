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
    
    # Load Derpibooru database dump
    IsDerpibooruDbNeeded = False
    for CurrentTag in dctTarget.keys() :
        if CurrentTag.startswith("ship:") :
            IsDerpibooruDbNeeded = True
            break
        #End If
    #Next
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
    #End If
    
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
        elif CurrentTag.startswith("ship:") :
            try :
                # Find shipping couple tags by indexing images
                print(f"    Ship tag: {CurrentTag}")
                iCurrentShipTag = dctTagsByName[CurrentTag]["Id"]
                arrTagIntersection = []
                for CurrentImg in dctImageTags.keys() :
                    if CurrentImg in dctImageHides.keys() :
                        continue
                    #End If
                    arrTagIds = dctImageTags[CurrentImg]
                    arrTagIntersection = IntersectArrays(arrTagIntersection, arrTagIds, sEmptyListOperation="keep")
                #Next
                print(f"        Intersected tag IDs: {arrTagIntersection}")
                
                # Map tag intersection to text
                arrTagIntersectionStr = []
                for CurrentId in arrTagIntersection :
                    if dctTagsById[CurrentId]["Category"] is None :
                        continue
                    elif dctTagsById[CurrentId]["Category"].lower() == "character" :
                        arrTagIntersectionStr.append(dctTagsById[CurrentId]["Name"])
                    elif dctTagsById[CurrentId]["Name"].startswith("oc:") :
                        arrTagIntersectionStr.append(dctTagsById[CurrentId]["Name"])
                    #End If
                #Next
                print(f"        Intersected tag names: {arrTagIntersectionStr}")
                
                # Translating
                sResult = "cp:"
                for i in range(0, len(arrTagIntersectionStr)) :
                    if arrTagIntersectionStr[i].startswith("oc:") :
                        if arrTagIntersectionStr[i] in dctTrans.keys() :
                            sResult = sResult + dctTrans[arrTagIntersectionStr[i]]["TransCn"][0].removeprefix("oc:")
                        else :
                            sResult = sResult + arrTagIntersectionStr[i].removeprefix("oc:") + "（OC）"
                        #End If
                    else :
                        if arrTagIntersectionStr[i] in dctTrans.keys() :
                            sResult = sResult + dctTrans[arrTagIntersectionStr[i]]["TransCn"][0]
                        else :
                            sResult = sResult + arrTagIntersectionStr[i]
                        #End If
                    #End If
                    if i < len(arrTagIntersectionStr)-1 :
                        sResult = sResult + "x"
                    #End If
                #Next
                print(f"        Proposed result: {sResult}")
                
                # Outputting
                dctTarget[CurrentTag]["TransCn"] = [f"{sResult}"]
                nProcessed += 1
            except :
                nSkipped += 1
            #End Try
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