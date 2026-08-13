import time

import pgdumplib

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
            tblTagTable = self._dmpDumpData.table_data("public", "tags")
            for CurrentTag in tblTagTable :
                dctCurrentTagInfo = dict(Id=0, ImageCount=0, Name="", Slug="", Category="")
                dctCurrentTagInfo["Id"] = int(CurrentTag[0])
                dctCurrentTagInfo["ImageCount"] = int(CurrentTag[1])
                dctCurrentTagInfo["Name"] = CurrentTag[2]
                dctCurrentTagInfo["Slug"] = CurrentTag[3]
                dctCurrentTagInfo["Category"] = CurrentTag[4]
                
                self._dctTagInfoByName[dctCurrentTagInfo["Name"]] = dctCurrentTagInfo
                self._dctTagInfoById[dctCurrentTagInfo["Id"]] = dctCurrentTagInfo
            #Next
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
            self._IsImageTagsLoaded = True
        #End If
        
        return self._dctImageTags
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

#End Class