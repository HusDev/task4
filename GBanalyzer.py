import pandas as pd
import numpy as np
import operator
import csv
from collections import Counter


# FUNCTION
# switch case function
def id_name_mapping(argument):
    switcher = {
        1:"Film & Animation",
        2:"Autos & Vehicles",
        10:"Music",
        15:"Pets & Animals",
        17:"Sports",
        18:"Short Movies",
        19:"Travel & Events",
        20:"Gaming",
        21:"Videoblogging",
        22:"People & Blogs",
        23:"Comedy",
        24:"Entertainment",
        25:"News & Politics",
        26:"Howto & Style",
        27:"Education",
        28:"Science & Technology",
        30:"Movies",
        31:"Anime/Animation",
        32:"Action/Adventure",
        33:"Classics",
        34:"Comedy",
        35:"Documentary",
        36:"Drama",
        37:"Family",
        38:"Foreign",
        39:"Horror",
        40:"Sci-Fi/Fantasy",
        41:"Thriller",
        42:"Shorts",
        43:"Shows",
        44:"Trailers"
}
    return switcher.get(argument, "nothing")

# counter function 
def count_occurrence(row_num):
    array = []
    with open('GB/GBvideos.csv','r',newline='') as f:
      reader = csv.reader(f)
    
      for row in reader:
        array.append(row[row_num])

    count = Counter(array) 
   
    return  count

# -----------------------------------------


data = pd.read_csv("GB/GBvideos.csv")
c_data = data.groupby('video_id').max()
c2_data = data.loc[data.duplicated(keep="last"),:]

# divition on zero
mask = c_data['dislikes'] > 0
c_data["ratio"] = np.where(mask, c_data['likes'] / c_data['dislikes'], 0)

# STEP1
# reactions
by_likes = c_data.sort_values("likes")
by_dislikes = c_data.sort_values("dislikes")
by_comments = c_data.sort_values("comment_count")
by_ratio = c_data.sort_values("ratio")

by_likes.to_csv("GB/reactions/by_likes.csv")
by_dislikes.to_csv("GB/reactions/by_dislikes.csv")
by_comments.to_csv("GB/reactions/by_comments.csv")
by_ratio.to_csv("GB/reactions/by_ratio.csv")

# STEP2
# Exposure
by_views = c_data.sort_values("views")
by_views.views.to_csv("GB/exposure/by_views.csv")


# sort_views = sorted(data,key=operator.itemgetter(0))
count = count_occurrence(2)
ar=[]
for k, v in count.items():
    ar.append(str(v)+","+k)
# sort array
sorted_ar = sorted(ar,key=operator.itemgetter(0))

with open('GB/exposure/by_streaks.csv','w',newline='') as new_file:
    csv_writer = csv.writer(new_file)
    for line in sorted_ar:
        csv_writer.writerow([line])

#STEP3 
# Category
file = open("GB/GBvideos.csv",newline='')
reader = csv.reader(file)
header = next(reader)


data_array =[]
for row in reader:
    # row = ['video_id', 'trending_date', 'title', 'channel_title', 'category_id', 'publish_time', 'tags', 'views', 'likes', 'dislikes', 'comment_count', 'thumbnail_link', 'comments_disabled', 'ratings_disabled', 'video_error_or_removed', 'description']
    video_id = row[0]
    trending_date = row[1]
    title = row[2]
    channel_title = row[3]
    category_id = int(row[4]) 
    publish_time = row[5]
    tags = row[6]
    views = int(row[7])
    likes = int(row[8])
    dislikes = int(row[9])
    comment_count = int(row[10])
    thumbnail_link = row[11]
    comments_disabled = row[12]
    ratings_disabled = row[13]
    video_error_or_removed = row[14]
    description = row[15]

    # addtions column
    if dislikes != 0:
        ratio = likes/dislikes
        
    
    data_array.append([video_id,trending_date,title,
                channel_title,category_id,
                publish_time,tags,views,
                likes,dislikes,comment_count,
                thumbnail_link,comments_disabled,ratings_disabled,
                video_error_or_removed,description,ratio])


sort_category = sorted(data_array,key=operator.itemgetter(4))
with open('GB/category/by_category.csv','w',newline='') as new_file:
    csv_writer = csv.writer(new_file,delimiter=' ')
    csv_writer.writerow(["id"+","+"category_name"+","+"videos"])
    for line in sort_category:
        category_name = id_name_mapping(line[4])    
        csv_writer.writerow([str(line[4]) + ","+ category_name +"," + str(line[3])])

# STEP3 TAGS
c2_data = data.loc[data.tags.duplicated(keep="last")]
# c2_data = data.loc[data.video_id.duplicated(keep="last")]

# c2_data["tags"].value_counts()
l = list(c2_data["tags"].values)

l[0].replace(",","|")
l = (",".join(l))

l=l.split('|')
y = [i.strip('"') for i in l]

count = Counter(y)
tag_count=[]
tag_name=[]
for k, v in count.items():
    tag_count.append(v)
    tag_name.append(k)
by_mentions=pd.DataFrame({"tag_count":tag_count,"tag_name":tag_name}).sort_values("tag_count")
by_mentions.to_csv("GB/tags/by_mentions.csv",index=False)

tag_by_cat = c2_data.sort_values("category_id")
tag_by_cat = tag_by_cat.loc[:,["category_id","tags"]]
tag_by_cat.to_csv("GB/tags/tag_by_cat.csv")

# by likes
# by virw
tags_data = data.groupby('tags').max()

tags_by_likes = tags_data.sort_values("likes")
tags_by_likes.to_csv("GB/tags/tags_by_likes.csv")

tags_by_views=tags_data.sort_values("views")
tags_by_views.to_csv("GB/tags/tags_by_views.csv")