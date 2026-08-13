# Splitting string with given separator, and remove empty results if requested
def SplitString(sStringToSplit : str, sSeparator : str = None, nMaxSplitCount : int = -1, RemoveEmptyEntries : bool = False) -> list :
    # Split string
    arrResult = sStringToSplit.split(sep=sSeparator, maxsplit=nMaxSplitCount)

    # Remove empty enrties
    if RemoveEmptyEntries :
        arrResult = list(filter(None, arrResult))
    #End If

    return arrResult
#End Function

# Load translated tags
def LoadTranslatedTags(sFile : str) -> dict :
    dctTags = dict()
    nProcessdTags = 0
    
    with open(sFile, "r", encoding="utf-8") as filTranslation :
        print(f"Loaded translation file {sFile}")
        
        arrLines = filTranslation.readlines()
        sLines = "\n".join(arrLines)
        arrTraslationLines = SplitString(sLines, " // A:")
        nTranslatedTags = len(arrTraslationLines)
        print(f"{nTranslatedTags} tag translation entries found")
        
        for CurrentTrans in arrTraslationLines :
            arrTagSeparated = SplitString(CurrentTrans, " - B:")
            arrTransSeparated = SplitString(arrTagSeparated[1], " - C:")
            sTag = arrTagSeparated[0].removeprefix("A:").removeprefix("\"").removesuffix("\"")
            sTrans = arrTransSeparated[0].removeprefix("\"").removesuffix("\"")
            sDesc = arrTransSeparated[1].removeprefix("\"").removesuffix("\"")
            
            dctCurrentTrans = dict(TransCn=[], Desc="")
            dctCurrentTrans["TransCn"] = SplitString(sTrans, ",")
            dctCurrentTrans["Desc"] = sDesc
            dctTags[sTag] = dctCurrentTrans
            nProcessdTags += 1
        #Next
        print(f"{nProcessdTags} tag(s) processed")
    #End With
    
    return dctTags
#End Function