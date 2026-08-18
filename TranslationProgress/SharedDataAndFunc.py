import os
import copy

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
    if not IsFileOrDirectoryExists(sPath) :
        return None
    #End If
    with open(sPath, "rb") as filObjDump :
        objInstance = pickle.load(filObjDump)
    #End With
    return objInstance
#End Function

# Get data from indexable object with fallbacks
def GetDataAtIndex(objDataSource, objIndex, objFallback = None) -> object :
    try :
        return objDataSource[objIndex]
    except :
        return objFallback
    #End Try
#End Function

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

# Uniforming path strings
def UniformPathString(sPathString : str, IsPathToDirectory : bool = False, IsPlatformCheckingsSkipped : bool = False) -> str :
    # Replace backslashes ("\") with slashes ("/") for compatibility with UNIX-like systems
    sUniformedPath = sPathString.replace("\\", "/")

    # Remove potential leading "\\?\" mark in Windows Unicode path
    if sUniformedPath.startswith("//?/UNC") :
        sUniformedPath = sUniformedPath.removeprefix("//?")
    elif sUniformedPath.startswith("//?/") :
        sUniformedPath = sUniformedPath.removeprefix("//?/")
    #End If

    # add a slash if it's path to a directory
    if IsPathToDirectory :
        if not sUniformedPath.endswith("/") :
            sUniformedPath = sUniformedPath + "/"
        #End If
    #End If
    
    # Convert path to platform-dependent form
    if not IsPlatformCheckingsSkipped :
        sUniformedPath = ConvertPathToWindowsUnicodePath(sUniformedPath)
    #End If

    return sUniformedPath
#End Function

# Convert full path to Windows Unicode path
# In order to bypass Windows long path limitation
# Ref. https://learn.microsoft.com/zh-cn/windows/win32/fileio/maximum-file-path-limitation
def ConvertPathToWindowsUnicodePath(sPathString : str, IsPlatformCheckingsBypassed : bool = False) -> str :
    # By default, this function only works on Windows
    # Only when IsPlatformCheckingsBypassed is set to True explicitly
    # On other platforms, will return the given path string with no modification
    sProcessedPath = sPathString
    if IsRunningOnWindows() or IsPlatformCheckingsBypassed :
        # Replace all "/" with "\"
        sProcessedPath = sProcessedPath.replace("/", "\\")
        
        # Check if current path could be converted to Unicode form safely
        # Only FULL path (starts with drive letters like "C:\") or UNC path (starts with \UNC\) could be processed safely
        if ((sProcessedPath[1] == ":" and sProcessedPath[2] == "\\")) or (sProcessedPath.startswith("\\UNC\\")) :
            # Add "\\?\" prefix
            if not sProcessedPath.startswith("\\\\?\\") :
                if sProcessedPath.startswith("\\?\\") :
                    sProcessedPath = "\\" + sProcessedPath
                elif sProcessedPath.startswith("?\\") :
                    sProcessedPath = "\\\\" + sProcessedPath
                elif sProcessedPath.startswith("\\") :
                    sProcessedPath = "\\\\?" + sProcessedPath
                else :
                    sProcessedPath = "\\\\?\\" + sProcessedPath
                #End If
            #End If
        #End If
    #End If
    return sProcessedPath
#End Function

# Get parent directory of a given path
def GetParentDirectory(sPathString : str, IsPlatformCheckingsSkipped : bool = False) -> str :
    # Get list of directories
    sPathString = UniformPathString(sPathString, IsPlatformCheckingsSkipped=True)
    arrDirList = SplitString(sStringToSplit=sPathString, sSeparator="/", RemoveEmptyEntries=True)

    # Generate path to parent directory
    sParentPath = ""
    for i in range(0, len(arrDirList) - 1) :
        sParentPath = sParentPath + arrDirList[i] + "/"
    #End If
    
    # Convert path to platform-dependent form
    if not IsPlatformCheckingsSkipped :
        sParentPath = ConvertPathToWindowsUnicodePath(sParentPath)
    #End If
    
    return sParentPath
#End Function

# Replace illegal characters in file name
def ReplaceInvalidFileNameChar(sFileName : str, sReplaceTo : str = "_") -> str :
    sValidFileName = sFileName
    sValidFileName = sValidFileName.replace("/", sReplaceTo)
    sValidFileName = sValidFileName.replace("\\", sReplaceTo)
    sValidFileName = sValidFileName.replace(":", sReplaceTo)
    sValidFileName = sValidFileName.replace("*", sReplaceTo)
    sValidFileName = sValidFileName.replace("?", sReplaceTo)
    sValidFileName = sValidFileName.replace("\"", sReplaceTo)
    sValidFileName = sValidFileName.replace("|", sReplaceTo)

    return sValidFileName
#End Function

# Get extension name from path
def GetExtensionNameFromPath(sPath : str) -> str :
    return sPath.removeprefix(os.path.splitext(sPath)[0])
#End Function

# Remove extension name from path
def RemoveExtensionNameFromPath(sPath : str) -> str :
    return os.path.splitext(sPath)[0]
#End Function

# Get current script's working directory
# Ref. https://blog.csdn.net/nixiang_888/article/details/109174340
def GetCurrentScriptWorkingDir(sTarget : str = "") -> str :
    sTarget = sTarget.upper()

    if sTarget == "CMDLINE" :
        sPath = os.getcwd()
        return UniformPathString(sPathString=sPath, IsPathToDirectory=True)
    elif sTarget == "ROOTSCRIPT" :
        sPath = sys.path[0]
        return UniformPathString(sPathString=sPath, IsPathToDirectory=True)
    elif sTarget == "THISSCRIPT" :
        sPath = os.path.split(os.path.realpath(__file__))[0]
        return UniformPathString(sPathString=sPath, IsPathToDirectory=True)
    else :
        sPath = os.getcwd()
        return UniformPathString(sPathString=sPath, IsPathToDirectory=True)
    #End If
#End Function

# Check existence of file or directory
def IsFileOrDirectoryExists(sPath : str) :
    return os.path.exists(sPath)
#End Function

# Create nested directories
def CreateDirectory(sPath : str) :
    if not IsFileOrDirectoryExists(sPath) :
        os.makedirs(sPath, exist_ok=True)
    #End If
#End Sub

# Remove nested directories
def RemoveDirectory(sPath : str) :
    if IsFileOrDirectoryExists(sPath) :
        shutil.rmtree(sPath, ignore_errors=True)
    #End If
#End Sub