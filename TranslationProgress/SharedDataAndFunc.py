# Translated file
sTransFile = "tags_translated_1786981181742.jsonl"

# Derpibooru database dump
sDerpibooruDatabseDump = "derpibooru_public_dump_2026_08_15.pgdump"

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