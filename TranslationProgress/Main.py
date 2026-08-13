import os
import pickle

import matplotlib.pyplot as plt

import TranslatedTagsUtil as Trans
from DerpibooruDatabaseDump import DerpibooruDatabaseDump

if __name__ == "__main__" :
    # Load translations
    dctTrans = Trans.LoadTranslatedTags("tags_translated_1786620152090.txt")
    
    # Load Derpibooru database dump
    dbDerpibooru = DerpibooruDatabaseDump("derpibooru_public_dump_2026_08_13.pgdump")
    dbDerpibooru.PrintInfo()
    print("Getting tags ...")
    dctTagsByName = dbDerpibooru.GetTagsByName()
    dctTagsById = dbDerpibooru.GetTagsById()
    nTags = len(dctTagsById.keys())
    print(f"{nTags} tags found in database dump")
    print("Getting image tags ...")
    if os.path.exists("_Cache/dctImageTags.pkl") :
        with open("_Cache/dctImageTags.pkl", "rb") as filObjDump : 
            dctImageTags = pickle.load(filObjDump)
        #End With
    else :
        dctImageTags = dbDerpibooru.GetImageTags()
        with open("_Cache/dctImageTags.pkl", "wb") as filObjDump : 
            pickle.dump(dctImageTags, filObjDump)
        #End With
    #End If
    nImages = len(dctImageTags.keys())
    print(f"{nImages} images found in database dump")
    
    # Count tags
    print("Counting tags ...")
    nBuckets = 10000
    arrTagCount = [0 for i in range(0,nBuckets)]
    for CurrentTag in dctTagsById.keys() :
        if dctTagsById[CurrentTag]["ImageCount"] > 0 :
            iBucket = dctTagsById[CurrentTag]["ImageCount"]
            if iBucket >= nBuckets :
                iBucket = nBuckets - 1
            #End If
            arrTagCount[iBucket] += 1
        #End If
    #Next
    arrX = [str(i) for i in arrTagCount]
    arrX[-1] = ">=" + arrX[-1]
    plt.bar(arrX, arrTagCount)
    plt.title("Distribution of Derpibooru tag image count")
    plt.show()
    
    # Tag count histogram
    arrTagCount = []
    for CurrentTag in dctTagsById.keys() :
        if dctTagsById[CurrentTag]["ImageCount"] > 0 :
            arrTagCount.append(dctTagsById[CurrentTag]["ImageCount"])
        #End If
    #Next
    plt.hist(arrTagCount, bins=50, log=True)
    plt.title("Histogram of Derpibooru tag image count")
    plt.show()
    
    # Translation check
    print("Checking translation progress")
    dctImageTransInfo = dict()
    nTotalImg = 0
    n100TransImg = 0
    n90TransImg = 0
    n75TransImg = 0
    n50TransImg = 0
    n1TransImg = 0
    n0TransImg = 0
    for CurrentImg in dctImageTags.keys() :
        arrTagIds = dctImageTags[CurrentImg]
        nValidTags = 0
        nTranslatedTags = 0
        for CurrentTag in arrTagIds :
            sCurrentTagName = dctTagsById[CurrentTag]["Name"]
            sCurrentTagCategory = dctTagsById[CurrentTag]["Category"]
            if sCurrentTagCategory is None :
                nValidTags += 1
                if sCurrentTagName in dctTrans.keys() :
                    nTranslatedTags += 1
                #End If
            #End If
        #Next
        
        if nValidTags > 0 :
            nTotalImg += 1
            dctImageTransInfo[CurrentImg]["Tags"] = nValidTags
            dctImageTransInfo[CurrentImg]["TransTags"] = nTranslatedTags
            if nTranslatedTags == nValidTags :
                n100TransImg += 1
            elif nTranslatedTags >= nValidTags * 0.9 :
                n90TransImg += 1
            elif nTranslatedTags >= nValidTags * 0.75 :
                n75TransImg += 1
            elif nTranslatedTags >= nValidTags * 0.5 :
                n50TransImg += 1
            elif nTranslatedTags >= 1 :
                n1TransImg += 1
            elif nTranslatedTags >= 0 :
                n0TransImg += 1
            #End If
        #End If
    #Next
    arrLabels = ["Full", "90%", "75%", "50%", "1 Tag", "None"]
    arrPct = [n100TransImg/nTotalImg, n90TransImg/nTotalImg, n75TransImg/nTotalImg, n50TransImg/nTotalImg, n1TransImg/nTotalImg, n0TransImg/nTotalImg]
    plt.pie(arrPct, labels=arrLabels, autopct="%.2f%%")
    plt.title("Tag translation distribution by image")
    plt.show()
#End If