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
    sTragetFile = "Job:Flat"
    sProcessedFile = "tags_trans_output.jsonl"
    dctTarget = dict()
    
    # Load Derpibooru database dump
    IsDerpibooruDbNeeded = True
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
    elif sTragetFile.lower() == "Job:Butt".lower() :
        iButtTagId = dctTagsByName["butt"]["Id"]
        for CurrentTagId in dctTagImpl.keys() :
            sCurrentTag = dctTagsById[CurrentTagId]["Name"]
            if sCurrentTag in dctTrans.keys() :
                continue
            #End If
            
            arrCurrentImpl = dctTagImpl[CurrentTagId]
            
            if iButtTagId in arrCurrentImpl :
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
                    if SubTagId != iButtTagId :
                        if (not (dctTagsById[SubTagId]["Category"] is None)) and (dctTagsById[SubTagId]["Category"].lower() == "character") :
                            sCurrentBaseTag = dctTagsById[SubTagId]["Name"]
                            print(f"Hit tag: {sCurrentTag}, base tag: {sCurrentBaseTag}")
                            dctCurrentTag = dict(TransCn=[], Desc="")
                            if sCurrentBaseTag in dctTrans.keys() :
                                for CurrentTrans in dctTrans[sCurrentBaseTag]["TransCn"] :
                                    dctCurrentTag["TransCn"].append(f"{CurrentTrans}的屁股")
                                #Next
                            else :
                                dctCurrentTag["TransCn"].append(f"{sCurrentBaseTag}的屁股")
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
    elif sTragetFile.lower() == "Job:ButtOC".lower() :
        iButtTagId = dctTagsByName["butt"]["Id"]
        for CurrentTagId in dctTagImpl.keys() :
            sCurrentTag = dctTagsById[CurrentTagId]["Name"]
            if sCurrentTag in dctTrans.keys() :
                continue
            #End If
            
            arrCurrentImpl = dctTagImpl[CurrentTagId]
            
            if iButtTagId in arrCurrentImpl :
                nCharacterCount = 0
                for SubTagId in arrCurrentImpl :
                    if dctTagsById[SubTagId]["Name"].startswith("oc:") :
                        nCharacterCount += 1
                    #End If
                #Next
                if nCharacterCount != 1 :
                    continue
                #End If
            
                for SubTagId in arrCurrentImpl :
                    if SubTagId != iButtTagId :
                        if dctTagsById[SubTagId]["Name"].startswith("oc:") :
                            sCurrentBaseTag = dctTagsById[SubTagId]["Name"]
                            print(f"Hit tag: {sCurrentTag}, base tag: {sCurrentBaseTag}")
                            dctCurrentTag = dict(TransCn=[], Desc="")
                            if sCurrentBaseTag in dctTrans.keys() :
                                for CurrentTrans in dctTrans[sCurrentBaseTag]["TransCn"] :
                                    dctCurrentTag["TransCn"].append(f"{CurrentTrans.removeprefix('oc:')}的屁股")
                                #Next
                            else :
                                dctCurrentTag["TransCn"].append(f"{sCurrentBaseTag.removeprefix('oc:')}（OC）的屁股")
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
    elif sTragetFile.lower() == "Job:Fat".lower() :
        iFatTagId = dctTagsByName["fat"]["Id"]
        for CurrentTagId in dctTagImpl.keys() :
            sCurrentTag = dctTagsById[CurrentTagId]["Name"]
            if sCurrentTag in dctTrans.keys() :
                continue
            #End If
            
            arrCurrentImpl = dctTagImpl[CurrentTagId]
            
            if iFatTagId in arrCurrentImpl :
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
                    if SubTagId != iFatTagId :
                        if (not (dctTagsById[SubTagId]["Category"] is None)) and (dctTagsById[SubTagId]["Category"].lower() == "character") :
                            sCurrentBaseTag = dctTagsById[SubTagId]["Name"]
                            print(f"Hit tag: {sCurrentTag}, base tag: {sCurrentBaseTag}")
                            dctCurrentTag = dict(TransCn=[], Desc="")
                            if sCurrentBaseTag in dctTrans.keys() :
                                for CurrentTrans in dctTrans[sCurrentBaseTag]["TransCn"] :
                                    dctCurrentTag["TransCn"].append(f"肥胖的{CurrentTrans}")
                                #Next
                            else :
                                dctCurrentTag["TransCn"].append(f"肥胖的{sCurrentBaseTag}")
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
    elif sTragetFile.lower() == "Job:Flat".lower() :
        iFlatTagId = dctTagsByName["delicious flat chest"]["Id"]
        for CurrentTagId in dctTagImpl.keys() :
            sCurrentTag = dctTagsById[CurrentTagId]["Name"]
            if sCurrentTag in dctTrans.keys() :
                continue
            #End If
            
            arrCurrentImpl = dctTagImpl[CurrentTagId]
            
            if iFlatTagId in arrCurrentImpl :
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
                    if SubTagId != iFlatTagId :
                        if (not (dctTagsById[SubTagId]["Category"] is None)) and (dctTagsById[SubTagId]["Category"].lower() == "character") :
                            sCurrentBaseTag = dctTagsById[SubTagId]["Name"]
                            print(f"Hit tag: {sCurrentTag}, base tag: {sCurrentBaseTag}")
                            dctCurrentTag = dict(TransCn=[], Desc="")
                            if sCurrentBaseTag in dctTrans.keys() :
                                for CurrentTrans in dctTrans[sCurrentBaseTag]["TransCn"] :
                                    dctCurrentTag["TransCn"].append(f"平胸{CurrentTrans}")
                                #Next
                            else :
                                dctCurrentTag["TransCn"].append(f"平胸{sCurrentBaseTag}")
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