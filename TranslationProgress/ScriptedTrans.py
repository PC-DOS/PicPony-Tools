import os
import copy
import datetime
import pathlib

import numpy as np
import matplotlib.pyplot as plt

import SharedDataAndFunc as Shared
#import TranslatedTagsUtilPlainText as Trans
import TranslatedTagsUtilJSON as Trans
from DerpibooruDatabaseDump import DerpibooruDatabaseDump

if __name__ == "__main__" :
    # Load translations
    sTransFile = Shared.sTransFile
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
    sProcessedFileExt = "tags_trans_output_ext.jsonl"
    dctTarget = Trans.LoadTranslatedTags(sTragetFile)
    dctExtTarget = dict()
    
    # Load Derpibooru database dump
    IsDerpibooruDbNeeded = False
    for CurrentTag in dctTarget.keys() :
        if CurrentTag.startswith("ship:") :
            IsDerpibooruDbNeeded = True
            break
        #End If
        if CurrentTag.startswith("parents:") :
            IsDerpibooruDbNeeded = True
            break
        #End If
    #Next
    if IsDerpibooruDbNeeded :
        dbDerpibooru = DerpibooruDatabaseDump(Shared.sDerpibooruDatabseDump)
        dbDerpibooru.PrintInfo()
        sDerpibooruTimestamp = dbDerpibooru.GetTimestamp()
        print("Getting tags ...")
        dctTagsByName = dbDerpibooru.GetTagsByName()
        dctTagsById = dbDerpibooru.GetTagsById()
        nTags = len(dctTagsById.keys())
        print(f"{nTags} tags found in database dump")
        print("Getting image tags ...")
        dctImageTags = dbDerpibooru.GetImageTags()
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
            elif dctTagsByName[CurrentTag]["Id"] in dctTagImpl :
                print(f"    Using implications logic for {CurrentTag}")
                arrParentsStr = []
                arrParentsTrans = []
                for CurrentImplId in dctTagImpl[dctTagsByName[CurrentTag]["Id"]] :
                    sCurrentImpl = dctTagsById[CurrentImplId]["Name"]
                    if sCurrentImpl.startswith("parent:") :
                        sCurrentImplBase = sCurrentImpl.removeprefix("parent:")
                        arrParentsStr.append(sCurrentImplBase)
                        if sCurrentImplBase in dctTrans.keys() :
                            arrParentsTrans.append(dctTrans[sCurrentImplBase]["TransCn"])
                        else :
                            arrParentsTrans.append([sCurrentImplBase])
                        #End If
                    #End If
                #End If
                arrResult = Shared.JoinMultipleStringArray(arrParentsTrans, "x")
                arrResultParents = [f"亲代：{s}" for s in arrResult]
                print(f"    Propsed result: {arrResultParents}")
                dctTarget[CurrentTag]["TransCn"] = arrResultParents
                dctExtTarget[sBaseTag] = dict(TransCn=arrResult, Desc="")
                nProcessed += 1
            else :
                print(f"    Using image intersection logic for {CurrentTag}")
                iCurrentShipTag = dctTagsByName[CurrentTag]["Id"]
                dctTagCounter = dict()
                arrTagIntersection = []
                for CurrentImg in dctImageTags.keys() :
                    if CurrentImg in dctImageHides.keys() :
                        continue
                    #End If
                    arrTagIds = dctImageTags[CurrentImg]
                    if not (iCurrentShipTag in arrTagIds) :
                        continue
                    #End If
                    arrTagIntersection = Shared.IntersectArrays(arrTagIntersection, arrTagIds, sEmptyListOperation="keep")
                    for tag in arrTagIds :
                        if tag in dctTagCounter.keys() :
                            dctTagCounter[tag] += 1
                        else :
                            dctTagCounter[tag] = 1
                        #End If
                    #Next
                #Next
                
                # Get max count tags
                nMaxTagCount = min(10, len(dctTagCounter.keys()))
                arrTopTags = []
                for j in range(0, nMaxTagCount) :
                    iCurrentTag = max(dctTagCounter, key=dctTagCounter.get)
                    if not (iCurrentTag in arrTagIntersection) :
                        arrTagIntersection.append(iCurrentTag)
                    #End If
                    dctTagCounter[iCurrentTag] = -1
                    arrTopTags.append(dctTagsById[iCurrentTag]["Name"])
                #Next
                print(f"        Top tags: {arrTopTags}")
                print(f"        Intersected tag IDs: {arrTagIntersection}")
            
                # Map tag intersection to text
                arrTagIntersectionStrRaw = []
                arrTagIntersectionStr = []
                for CurrentId in arrTagIntersection :
                    arrTagIntersectionStrRaw.append(dctTagsById[CurrentId]["Name"])
                    if dctTagsById[CurrentId]["Category"] is None :
                        if dctTagsById[CurrentId]["Name"].startswith("parent:") :
                            arrTagIntersectionStr.append(dctTagsById[CurrentId]["Name"].removeprefix("parent:"))
                        else :
                            continue
                        #End If
                    elif dctTagsById[CurrentId]["Category"].lower() == "character" :
                        continue
                    elif dctTagsById[CurrentId]["Name"].startswith("oc:") :
                        continue
                    #End If
                #Next
                arrObjToRemove = []
                for i in range(0, len(arrTagIntersectionStr)) :
                    for j in range(0, len(arrTagIntersectionStr)) :
                        if i == j :
                            continue
                        #End If
                        if dbDerpibooru.IsTagImplies(arrTagIntersectionStr[i], arrTagIntersectionStr[j]) :
                            arrObjToRemove.append(arrTagIntersectionStr[j])
                        #End If
                    #Next
                #Next
                for s in arrObjToRemove :
                    if s in arrTagIntersectionStr :
                        arrTagIntersectionStr.remove(s)
                    #End If
                #Next
                print(f"        Intersected tag names: {arrTagIntersectionStrRaw}")
                print(f"        Intersected tag names (character & oc only): {arrTagIntersectionStr}")
                if len(arrTagIntersectionStr) <= 1 :
                    nSkipped += 1
                    continue
                #End If
                
                # Translating
                arrTranslatedTags = []
                arrResult = []
                for i in range(0, len(arrTagIntersectionStr)) :
                    arrCurrentTagTrans = []
                    if arrTagIntersectionStr[i].startswith("oc:") :
                        if arrTagIntersectionStr[i] in dctTrans.keys() :
                            arrCurrentTagTrans = [s.removeprefix("oc:") for s in dctTrans[arrTagIntersectionStr[i]]["TransCn"]]
                        else :
                            arrCurrentTagTrans = [arrTagIntersectionStr[i].removeprefix("oc:") + "（OC）"]
                        #End If
                    else :
                        if arrTagIntersectionStr[i] in dctTrans.keys() :
                            arrCurrentTagTrans = [s for s in dctTrans[arrTagIntersectionStr[i]]["TransCn"]]
                        else :
                            arrCurrentTagTrans = [arrTagIntersectionStr[i]]
                        #End If
                    #End If
                    arrTranslatedTags.append(arrCurrentTagTrans)
                #Next
                arrResult = Shared.JoinMultipleStringArray(arrTranslatedTags, "x")
                arrResultShip = [f"亲代：{s}" for s in arrResult]
                print(f"        Proposed result: {arrResultShip}")
                
                # Outputting
                dctTarget[CurrentTag]["TransCn"] = arrResultShip
                dctExtTarget[sBaseTag] = dict(TransCn=arrResult, Desc="")
                nProcessed += 1
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
                nSkipped += 1
                #dctTarget[CurrentTag]["TransCn"] = [f"融合：{sBaseTag}"]
                #nProcessed += 1
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
        elif CurrentTag.startswith("busty oc:") :
            sBaseTag = CurrentTag.removeprefix("busty oc:")
            if "oc:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["oc:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"丰满的{CurrentSource.removeprefix('oc:')}")
                    dctTarget[CurrentTag]["TransCn"].append(f"丰乳{CurrentSource.removeprefix('oc:')}")
                #Next
                nProcessed += 1
            else :
                dctTarget[CurrentTag]["TransCn"] = [f"丰满的{sBaseTag}（OC）", f"丰乳{sBaseTag}（OC）"]
                nProcessed += 1
            #End If
        elif CurrentTag.startswith("busty ") :
            sBaseTag = CurrentTag.removeprefix("busty ")
            if sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans[sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"丰满的{CurrentSource}")
                    dctTarget[CurrentTag]["TransCn"].append(f"丰乳{CurrentSource}")
                #Next
                nProcessed += 1
            elif "oc:"+sBaseTag in dctTrans.keys() :
                arrCurrentSource = dctTrans["oc:"+sBaseTag]["TransCn"]
                dctTarget[CurrentTag]["TransCn"] = []
                for CurrentSource in arrCurrentSource :
                    dctTarget[CurrentTag]["TransCn"].append(f"丰满的{CurrentSource.removeprefix('oc:')}")
                    dctTarget[CurrentTag]["TransCn"].append(f"丰乳{CurrentSource.removeprefix('oc:')}")
                #Next
                nProcessed += 1
            else :
                dctTarget[CurrentTag]["TransCn"] = [f"丰满的{sBaseTag}", f"丰乳{sBaseTag}"]
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
            #try :
            # Find shipping couple tags by indexing images
            print(f"    Ship tag: {CurrentTag}")
            iCurrentShipTag = dctTagsByName[CurrentTag]["Id"]
            if not (dctTagsByName[CurrentTag]["ShortDesc"] is None) :
                sCurrentTagShortDesc = dctTagsByName[CurrentTag]["ShortDesc"].lower().removesuffix(" shipping")
            else :
                sCurrentTagShortDesc = ""
            #End If
            arrCurrentTagShortDesc = sCurrentTagShortDesc.split(" x ")
            IsShortDescParsed = False
            arrTagIntersection = []
            for s in arrCurrentTagShortDesc :
                if s in dctTagsByName.keys() :
                    arrTagIntersection.append(dctTagsByName[s]["Id"])
                    IsShortDescParsed = True
                else :
                    IsShortDescParsed = False
                    break
                #End If
            #Next
            if (len(arrTagIntersection) <= 1) or (not IsShortDescParsed) :
                if iCurrentShipTag in dctTagImpl.keys() :
                    arrTagIntersection = dctTagImpl[iCurrentShipTag]
                else :
                    dctTagCounter = dict()
                    for CurrentImg in dctImageTags.keys() :
                        if CurrentImg in dctImageHides.keys() :
                            continue
                        #End If
                        arrTagIds = dctImageTags[CurrentImg]
                        if not (iCurrentShipTag in arrTagIds) :
                            continue
                        #End If
                        arrTagIntersection = Shared.IntersectArrays(arrTagIntersection, arrTagIds, sEmptyListOperation="keep")
                        for tag in arrTagIds :
                            if tag in dctTagCounter.keys() :
                                dctTagCounter[tag] += 1
                            else :
                                dctTagCounter[tag] = 1
                            #End If
                        #Next
                    #Next
                    
                    # Get max count tags
                    nMaxTagCount = min(10, len(dctTagCounter.keys()))
                    arrTopTags = []
                    for j in range(0, nMaxTagCount) :
                        iCurrentTag = max(dctTagCounter, key=dctTagCounter.get)
                        if not (iCurrentTag in arrTagIntersection) :
                            arrTagIntersection.append(iCurrentTag)
                        #End If
                        dctTagCounter[iCurrentTag] = -1
                        arrTopTags.append(dctTagsById[iCurrentTag]["Name"])
                    #Next
                    print(f"        Top tags: {arrTopTags}")
                #End If
            #End If
            print(f"        Intersected tag IDs: {arrTagIntersection}")
            
            # Map tag intersection to text
            arrTagIntersectionStrRaw = []
            arrTagIntersectionStr = []
            for CurrentId in arrTagIntersection :
                arrTagIntersectionStrRaw.append(dctTagsById[CurrentId]["Name"])
                if IsShortDescParsed :
                    arrTagIntersectionStr.append(dctTagsById[CurrentId]["Name"])
                elif dctTagsById[CurrentId]["Category"] is None :
                    if dctTagsById[CurrentId]["Name"].startswith("ship:") or ("shipping" in dctTagsById[CurrentId]["Name"]) :
                        continue
                    elif dctTagsById[CurrentId]["Name"].startswith("busty ") :
                        continue
                    elif (CurrentId in dctTagImpl.keys()) and (dctTagsByName["rule 63"]["Id"] in dctTagImpl[CurrentId]) :
                        arrTagIntersectionStr.append(dctTagsById[CurrentId]["Name"])
                    else :
                        continue
                    #End If
                elif dctTagsById[CurrentId]["Category"].lower() == "character" :
                    arrTagIntersectionStr.append(dctTagsById[CurrentId]["Name"])
                elif dctTagsById[CurrentId]["Name"].startswith("oc:") :
                    arrTagIntersectionStr.append(dctTagsById[CurrentId]["Name"])
                #End If
            #Next
            arrObjToRemove = []
            for i in range(0, len(arrTagIntersectionStr)) :
                for j in range(0, len(arrTagIntersectionStr)) :
                    if i == j :
                        continue
                    #End If
                    if dbDerpibooru.IsTagImplies(arrTagIntersectionStr[i], arrTagIntersectionStr[j]) :
                        arrObjToRemove.append(arrTagIntersectionStr[j])
                    #End If
                #Next
            #Next
            for s in arrObjToRemove :
                if s in arrTagIntersectionStr :
                    arrTagIntersectionStr.remove(s)
                #End If
            #Next
            print(f"        Intersected tag names: {arrTagIntersectionStrRaw}")
            print(f"        Intersected tag names (character & oc only): {arrTagIntersectionStr}")
            if len(arrTagIntersectionStr) <= 1 :
                nSkipped += 1
                continue
            #End If
            
            # Translating
            arrTranslatedTags = []
            arrResult = []
            for i in range(0, len(arrTagIntersectionStr)) :
                arrCurrentTagTrans = []
                if arrTagIntersectionStr[i].startswith("oc:") :
                    if arrTagIntersectionStr[i] in dctTrans.keys() :
                        arrCurrentTagTrans = [s.removeprefix("oc:") for s in dctTrans[arrTagIntersectionStr[i]]["TransCn"]]
                    else :
                        arrCurrentTagTrans = [arrTagIntersectionStr[i].removeprefix("oc:") + "（OC）"]
                    #End If
                else :
                    if arrTagIntersectionStr[i] in dctTrans.keys() :
                        arrCurrentTagTrans = [s for s in dctTrans[arrTagIntersectionStr[i]]["TransCn"]]
                    else :
                        arrCurrentTagTrans = [arrTagIntersectionStr[i]]
                    #End If
                #End If
                arrTranslatedTags.append(arrCurrentTagTrans)
            #Next
            arrResult = Shared.JoinMultipleStringArray(arrTranslatedTags, "x")
            arrResultShip = [f"cp:{s}" for s in arrResult]
            print(f"        Proposed result: {arrResultShip}")
            
            # Outputting
            dctTarget[CurrentTag]["TransCn"] = arrResultShip
            nProcessed += 1
            #except :
            #    nSkipped += 1
            #End Try
            #input()
        else :
            nSkipped += 1
        #End If
        
        #dctTarget[CurrentTag]["Desc"] = ""
        nTotal += 1
    #Next
    print(f"Total: {nTotal}, Processed: {nProcessed}, Skipped: {nSkipped}")
    
    # Outputting
    Trans.ExportTranslatedTags(dctTarget, sProcessedFile)
    Trans.ExportTranslatedTags(dctExtTarget, sProcessedFileExt)
#End If