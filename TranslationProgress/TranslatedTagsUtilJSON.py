import json

import SharedDataAndFunc as Shared

# Load translated tags
def LoadTranslatedTags(sFile : str) -> dict :
    dctTags = dict()
    nProcessdTags = 0
    
    with open(sFile, "r", encoding="utf-8") as filTranslation :
        print(f"Loaded translation file {sFile}")
        
        arrLines = filTranslation.readlines()
        arrTraslationLines = arrLines
        nTranslatedTags = len(arrTraslationLines)
        print(f"{nTranslatedTags} tag translation entries found")
        
        for CurrentTrans in arrTraslationLines :
            dctCurrentTrans = json.loads(CurrentTrans)
            sTag = dctCurrentTrans["en"]
            arrTrans = [dctCurrentTrans["cn"]]
            sDesc = dctCurrentTrans["description"]
            
            arrAlias = dctCurrentTrans["aliases"]
            for CurrentAlias in arrAlias :
                arrTrans.append(CurrentAlias)
            #Next
            
            dctCurrentTrans = dict(TransCn=[], Desc="")
            dctCurrentTrans["TransCn"] = arrTrans
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
            arrTrans = dctTags[sTag]["TransCn"]
            nTransCount = len(arrTrans)
            sTrans = ""
            arrAlias = []
            for j in range(0, nTransCount) :
                if j == 0 :
                    sTrans = arrTrans[0]
                else :
                    arrAlias.append(arrTrans[j])
                #End If
            #Next
            sDesc = dctTags[sTag]["Desc"]
            dctCurrentTransToJson = dict(en=sTag, cn=sTrans, aliases=arrAlias, description=sDesc)
            sCurrentLine = json.dumps(dctCurrentTransToJson, ensure_ascii=False)
            sCurrentLine = sCurrentLine + "\n"
            filTranslation.write(sCurrentLine)
            nProcessdTags += 1
        #Next
        
        print(f"{nProcessdTags} tag(s) processed")
    #End With
#End Sub
    
