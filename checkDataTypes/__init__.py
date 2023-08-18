# -*- encoding : utf-8 -*-


from clssRAWDATATYPE import *


def mai():
    clsFRC = FILES('.parquet')
    clsFRC.list_Dir('.')
    for Attr, Value in clsFRC.kFiles.items():
        if Attr.lower().endswith(clsFRC._dotExts)
        for Files in Value:
            clsFRC = READ(Files,'.parquet')
            clsFRC = DATA(clsFRC.read_File(), Files, '.parquet')
            clsFRC.dissert_Datatypes()