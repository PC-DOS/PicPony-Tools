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
    print("Getting image tags ...")
    dctImages = dbDerpibooru.GetImageTags()
    nImages = len(dctImages.keys())
    nTags = len(dctTagsById.keys())
    print(f"{nImages} images and {nTags} tags found in database dump")
    
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
            arrTagCount[dctTagsById[CurrentTag]["ImageCount"]] += 1
        #End If
    #Next
    arrX = [str(i) for i in arrTagCount]
    arrX[-1] = ">=" + arrX[-1]
    plt.bar(arrX, arrTagCount)
    plt.title("Distribution of Derpibooru tag image count")
    plt.show()
#End If