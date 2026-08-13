import os
import pickle

import pgdumplib

class DerpibooruDatabaseDump() :
    
    # Constructor
    def __init__(self, sDumpFile : str, IsCachingEnabled : bool = True) :
        print(f"Loading dump file {sDumpFile} ...")
        self._sDumpPath = sDumpFile
        os.makedirs("Cache/")
        sCachepath = "Cache/" + sDumpFile.replace(":","_").replace("/","_").replace("\\","_").removesuffix(".pgdump") + ".pgdumpcache"
        if os.path.exists(sCachepath) and IsCachingEnabled :
            with open(sCachepath, "rb") as filObjDump :
                self._dmpDumpData = pickle.load(filObjDump)
            #End With
        else :
            self._dmpDumpData = pgdumplib.load(sDumpFile)
            if IsCachingEnabled :
                with open(sCachepath, "wb") as filObjDump :
                    pickle.dump(self._dmpDumpData, filObjDump)
                #End With
            #End If
        #End If
    #End Sub
    
    # Print info
    def PrintInfo(self) :
        print(f"Path: {self._sDumpPath}")
        print(f"Database: {self._dmpDumpData.dbname}")
        print(f"Archive Timestamp: {self._dmpDumpData.timestamp}")
        print(f"Server Version: {self._dmpDumpData.server_version}")
        print(f"Dump Version: {self._dmpDumpData.dump_version}")
    #End Sub
    
    # Get tags
    def GetTags(self, sIndexType : str = "name", IsReloadRequested : bool = False) -> dict :
        if (not self._IsTagsLoaded) or IsReloadRequested :
            tblTagTable = self._dmpDumpData.table_data("public", "tags")
            for CurrentTag in tblTagTable :
                print(CurrentTag)
                input()
                
                dctCurrentTagInfo = dict(Id=0, Name="", Category="", ImageCount="")
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
    
    # Get images
    def GetImages(self, IsReloadRequested : bool = False) -> dict :
        if (not self._IsImagesLoaded) or IsReloadRequested :
            tblImageTable = self._dmpDumpData.table_data("public", "images")
            for CurrentImage in tblImageTable :
                print(CurrentImage)
                input()
            #Next
            self._IsTagsLoaded = True
        #End If
        
        return self._dctImages
    #End Function
    
    # Properties
    
    # Internal variables
    _sDumpPath = ""
    _dmpDumpData = None
    # Tags
    _IsTagsLoaded = False
    _dctTagInfoById = dict()
    _dctTagInfoByName = dict()
    # Images
    _IsImagesLoaded = False
    _dctImages = dict()

#End Class