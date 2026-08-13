import matplotlib.pyplot as plt

import TranslatedTagsUtil as Trans
from DerpibooruDatabaseDump import DerpibooruDatabaseDump

if __name__ == "__main__" :
    # Load translations
    dctTrans = Trans.LoadTranslatedTags("tags_translated_1786620152090.txt")
    
    # Load Derpibooru database dump
    dbDerpibooru = DerpibooruDatabaseDump("derpibooru_public_dump_2026_08_13.pgdump")
    dbDerpibooru.PrintInfo()
    dctTagsByName = dbDerpibooru.GetTagsByName()
    
#End If