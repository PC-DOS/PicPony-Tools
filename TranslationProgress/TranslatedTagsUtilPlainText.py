import SharedDataAndFunc as Shared

# Load translated tags
def LoadTranslatedTags(sFile : str) -> dict :
    dctTags = dict()
    nProcessdTags = 0
    
    with open(sFile, "r", encoding="utf-8") as filTranslation :
        print(f"Loaded translation file {sFile}")
        
        arrLines = filTranslation.readlines()
        sLines = "\n".join(arrLines)
        arrTraslationLines = Shared.SplitString(sLines, " // A:")
        nTranslatedTags = len(arrTraslationLines)
        print(f"{nTranslatedTags} tag translation entries found")
        
        for CurrentTrans in arrTraslationLines :
            arrTagSeparated = Shared.SplitString(CurrentTrans, " - B:")
            arrTransSeparated = Shared.SplitString(arrTagSeparated[1], " - C:")
            sTag = arrTagSeparated[0].removeprefix("A:")
            sTrans = arrTransSeparated[0]
            sDesc = arrTransSeparated[1]
            
            dctCurrentTrans = dict(TransCn=[], Desc="")
            dctCurrentTrans["TransCn"] = Shared.SplitString(sTrans, ",")
            dctCurrentTrans["Desc"] = sDesc
            dctTags[sTag] = dctCurrentTrans
            nProcessdTags += 1
        #Next
        print(f"{nProcessdTags} tag(s) processed")
    #End With
    
    return dctTags
#End Function

# Export translated tags
def ExportTranslatedTags(dctTags : dict, sFile : str) :
    nProcessdTags = 0
    
    with open(sFile, "w", encoding="utf-8") as filTranslation :
        print(f"Writing translation to file {sFile}")
        
        arrTags = list(dctTags.keys())
        nTagCount = len(arrTags)
        print(f"{nTagCount} tag translation entries found")
        
        for i in range(0, nTagCount) :
            sTag = arrTags[i]
            sTrans = ",".join(dctTags[sTag]["TransCn"])
            sDesc = dctTags[sTag]["Desc"]
            sCurrentLine = f"A:{sTag} - B:{sTrans} - C:{sDesc}"
            if i < nTagCount - 1 :
                sCurrentLine = sCurrentLine + " // "
            #End If
            filTranslation.write(sCurrentLine)
            nProcessdTags += 1
        #Next
        
        print(f"{nProcessdTags} tag(s) processed")
    #End With
#End Sub
    
