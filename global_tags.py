import pandas as pd
import numpy as np
import operator
import csv
from collections import Counter

# Function
def tag_counter(name):
    name[0].replace(",","|")
    name = (",".join(name))

    name=name.split('|')
    y = [i.strip('"') for i in name]
    count = Counter(y)
    return count




USdata = pd.read_csv("US/USvideos.csv")
DEdata = pd.read_csv("DE/DEvideos.csv")
FRdata = pd.read_csv("FR/FRvideos.csv")
GBdata = pd.read_csv("GB/GBvideos.csv")
CAdata = pd.read_csv("CA/CAvideos.csv")

#c_data = clear data = unique data
c_USdata = USdata.loc[USdata.tags.duplicated(keep="last")] 
c_DEdata = DEdata.loc[DEdata.tags.duplicated(keep="last")] 
c_FRdata = FRdata.loc[FRdata.tags.duplicated(keep="last")] 
c_GBdata = GBdata.loc[GBdata.tags.duplicated(keep="last")] 
c_CAdata = CAdata.loc[CAdata.tags.duplicated(keep="last")] 


l_US = list(c_USdata["tags"].values) 
l_DE = list(c_DEdata["tags"].values) 
l_FR = list(c_FRdata["tags"].values) 
l_GB = list(c_GBdata["tags"].values) 
l_CA = list(c_CAdata["tags"].values) 

US_tags=tag_counter(l_US)
DE_tags=tag_counter(l_DE)
FR_tags=tag_counter(l_FR)
BG_tags=tag_counter(l_GB)
CA_tags=tag_counter(l_CA)



global_tags = [US_tags,DE_tags,FR_tags,BG_tags,CA_tags] 



tag_count=[]
tag_name=[]
for tags in global_tags:
    for k, v in tags.items():
        tag_count.append(v)
        tag_name.append(k)

by_mentions=pd.DataFrame({"tag_count":tag_count,"tag_name":tag_name}).sort_values("tag_count")
by_mentions.to_csv("global/by_mentions.csv",index=False)
