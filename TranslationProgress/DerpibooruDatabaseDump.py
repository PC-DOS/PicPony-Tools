import time
import os

import pgdumplib

import SharedDataAndFunc as Shared

class DerpibooruDatabaseDump() :
    
    # Constructor
    def __init__(self, sDumpFile : str) :
        print(f"Loading dump file {sDumpFile} ...")
        self._sDumpPath = sDumpFile
        dNsStart = time.perf_counter_ns()
        self._dmpDumpData = pgdumplib.load(sDumpFile)
        dNsEnd = time.perf_counter_ns()
        dNsDelay = dNsEnd - dNsStart
        dTimeElapsed = dNsDelay / 1000.0 / 1000.0 / 1000.0
        print(f"Dump file {sDumpFile} loaded in {round(dTimeElapsed, 2)} seconds")
        os.makedirs("_Cache/", exist_ok=True)
    #End Sub
    
    # Print info
    def PrintInfo(self) :
        print(f"Path: {self._sDumpPath}")
        print(f"Database: {self._dmpDumpData.dbname}")
        print(f"Archive Timestamp: {self._dmpDumpData.timestamp}")
        print(f"Server Version: {self._dmpDumpData.server_version}")
        print(f"Dump Version: {self._dmpDumpData.dump_version}")
    #End Sub
    
    def GetTimestamp(self) -> str :
        return self._dmpDumpData.timestamp
    #End Function
    
    # Get tags
    def GetTags(self, sIndexType : str = "name", IsReloadRequested : bool = False) -> dict :
        if (not self._IsTagsLoaded) or IsReloadRequested :
            tplTagInfo = Shared.LoadObjectFromFile("_Cache/tplTagInfo.pkl")
            if tplTagInfo is None :
                tblTagTable = self._dmpDumpData.table_data("public", "tags")
                for CurrentTag in tblTagTable :
                    dctCurrentTagInfo = dict(Id=0, ImageCount=0, Name="", Slug="", Category="", Desc="", ShortDesc="")
                    dctCurrentTagInfo["Id"] = int(CurrentTag[0])
                    dctCurrentTagInfo["ImageCount"] = int(CurrentTag[1])
                    dctCurrentTagInfo["Name"] = CurrentTag[2]
                    dctCurrentTagInfo["Slug"] = CurrentTag[3]
                    dctCurrentTagInfo["Category"] = Shared.GetDataAtIndex(CurrentTag, 4, None)
                    dctCurrentTagInfo["Desc"] = Shared.GetDataAtIndex(CurrentTag, 5, "")
                    dctCurrentTagInfo["ShortDesc"] = Shared.GetDataAtIndex(CurrentTag, 6, "")
                    
                    self._dctTagInfoByName[dctCurrentTagInfo["Name"]] = dctCurrentTagInfo
                    self._dctTagInfoById[dctCurrentTagInfo["Id"]] = dctCurrentTagInfo
                #Next
                tplTagInfo = (self._dctTagInfoByName, self._dctTagInfoById)
                Shared.DumpObjectToFile(tplTagInfo, "_Cache/tplTagInfo.pkl")
            #End If
            self._dctTagInfoByName = tplTagInfo[0]
            self._dctTagInfoById = tplTagInfo[1]
            self._IsTagsLoaded = True
        #End If
        
        if sIndexType.lower() == "name" :
            return self._dctTagInfoByName
        else :
            return self._dctTagInfoById
        #End If
    #End Function
    
    def GetTagsById(self, IsReloadRequested : bool = False) -> dict :
        return self.GetTags("id", IsReloadRequested)
    #End Function
    
    def GetTagsByName(self, IsReloadRequested : bool = False) -> dict :
        return self.GetTags("name", IsReloadRequested)
    #End Function
    
    # Get image tags
    def GetImageTags(self, IsReloadRequested : bool = False) -> dict :
        if (not self._IsImageTagsLoaded) or IsReloadRequested :
            self._dctImageTags = Shared.LoadObjectFromFile("_Cache/dctImageTags.pkl")
            if self._dctImageTags is None :
                tblImageTagTable = self._dmpDumpData.table_data("public", "image_taggings")
                self._dctImageTags = dict()
                for CurrentImage in tblImageTagTable :
                    iCurrentImageId = int(CurrentImage[0])
                    iCurrentImageTag = int(CurrentImage[1])
                    if not (iCurrentImageId in self._dctImageTags.keys()) :
                        self._dctImageTags[iCurrentImageId] = []
                    #End If
                    self._dctImageTags[iCurrentImageId].append(iCurrentImageTag)
                #Next
                Shared.DumpObjectToFile(self._dctImageTags, "_Cache/dctImageTags.pkl")
            #End If
            self._IsImageTagsLoaded = True
        #End If
        
        return self._dctImageTags
    #End Function
    
    # Get image hides
    def GetImageHides(self, IsReloadRequested : bool = False) -> dict :
        if (not self._IsImageHidesLoaded) or IsReloadRequested :
            self._dctImageHides = Shared.LoadObjectFromFile("_Cache/dctImageHides.pkl")
            if self._dctImageHides is None :
                tblImageHideTable = self._dmpDumpData.table_data("public", "image_hides")
                self._dctImageHides = dict()
                for CurrentImage in tblImageHideTable :
                    iCurrentImageId = int(CurrentImage[0])
                    sCurrentImageHideReason = Shared.GetDataAtIndex(CurrentImage, 1, "")
                    self._dctImageHides[iCurrentImageId] = sCurrentImageHideReason
                #Next
                Shared.DumpObjectToFile(self._dctImageHides, "_Cache/dctImageHides.pkl")
            #End If
            self._IsImageHidesLoaded = True
        #End If
        
        return self._dctImageHides
    #End Function
    
    # Get tag to image mapping
    def GetTagToImageMapping(self, IsReloadRequested : bool = False) -> dict :
        if (not self._IsTagToImageMappingLoaded) or IsReloadRequested :
            self._dctTagToImageMapping = Shared.LoadObjectFromFile("_Cache/dctTagToImageMapping.pkl")
            if _dctTagToImageMapping is None :
                tblImageTagTable = self._dmpDumpData.table_data("public", "image_taggings")
                self._dctTagToImageMapping = dict()
                for CurrentImage in tblImageTagTable :
                    iCurrentImageId = int(CurrentImage[0])
                    iCurrentImageTag = int(CurrentImage[1])
                    if not (iCurrentImageTag in self._dctTagToImageMapping.keys()) :
                        self._dctTagToImageMapping[iCurrentImageTag] = []
                    #End If
                    self._dctTagToImageMapping[iCurrentImageTag].append(iCurrentImageId)
                #Next
                Shared.DumpObjectToFile(self._dctTagToImageMapping, "_Cache/dctTagToImageMapping.pkl")
            #End If
            self._IsTagToImageMappingLoaded = True
        #End If
        
        return self._dctTagToImageMapping
    #End Function
    
    # Get tag to image mapping
    def GetTagImplications(self, IsReloadRequested : bool = False) -> dict :
        if (not self._IsTagImplicationsLoaded) or IsReloadRequested :
            self._dctTagImplications = Shared.LoadObjectFromFile("_Cache/dctTagImplications.pkl")
            if self._dctTagImplications is None :
                tblImageTagTable = self._dmpDumpData.table_data("public", "tag_implications")
                self._dctTagImplications = dict()
                for CurrentTag in tblImageTagTable :
                    iCurrentTagId = int(CurrentTag[0])
                    iCurrentTagTarget = int(CurrentTag[1])
                    if not (iCurrentTagId in self._dctTagImplications.keys()) :
                        self._dctTagImplications[iCurrentTagId] = []
                    #End If
                    self._dctTagImplications[iCurrentTagId].append(iCurrentTagTarget)
                #Next
                Shared.DumpObjectToFile(self._dctTagImplications, "_Cache/dctTagImplications.pkl")
            #End If
            self._IsTagImplicationsLoaded = True
        #End If
        
        return self._dctTagImplications
    #End Function
    
    # Check if sLeftTag implies
    def IsTagImplies(self, sLeftTag : str, sRightTag : str) -> bool :
        self.GetTagsById()
        self.GetTagImplications()
        try :
            iLeftTag = self._dctTagInfoByName[sLeftTag]["Id"]
            iRightTag = self._dctTagInfoByName[sRightTag]["Id"]
        except :
            return False
        #End Try
        
        if iLeftTag in self._dctTagImplications.keys() :
            return (iRightTag in self._dctTagImplications[iLeftTag])
        else :
            return False
        #End If
    #End Function
    
    # Properties
    
    # Internal variables
    _sDumpPath = ""
    _dmpDumpData = None
    # Tags
    _IsTagsLoaded = False
    _dctTagInfoById = dict()
    _dctTagInfoByName = dict()
    # Image tags
    _IsImageTagsLoaded = False
    _dctImageTags = dict()
    # Image hides
    _IsImageHidesLoaded = False
    _dctImageHides = dict()
    # Tag to image mapping
    _IsTagToImageMappingLoaded = False
    _dctTagToImageMapping = dict()
    # Tag implications
    _IsTagImplicationsLoaded = False
    _dctTagImplications = dict()

#End Class