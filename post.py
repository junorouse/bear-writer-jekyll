import os, re
from json import loads
import bear


def title_to_filename(title):
    """
    We build a simple filename from the title - i.e. "These Cats" becomes "these_cats.md". We do
    not check for existence, as we may be doing an overwrite deliberately.
    """

    name = re.sub(r'[^a-z0-9]','-',title.lower())+".md"
    return name

b = bear.Bear()

tag = b.tag_by_title('blog', 'desc')
notes = tag.notes() # notes is generator
note_list = []

try:
    for i in range(5):
        note_list.append(next(notes))
except:
    pass

for i in range(len(note_list)):
    print("{}. {}".format(i+1, note_list[i]))

idx = int(input("idx: ")) - 1

tags = [t.title for t in note_list[idx].tags()]

try:
    tags.remove("글쓰기")
except ValueError:
    pass

try:
    tags.remove("blog")
except ValueError:
    pass

data = ("""---
layout: "post"
comments: true
title: {}
date: {}
tags: {}
uuid: {}
---
{}""".format(note_list[idx].title, note_list[idx].created.strftime('%Y-%m-%d %H:%M:%S +0900'), ' '.join(tags), note_list[idx].id, '\n'.join(note_list[idx].text.split("\n")[1:-1])))

suffix_dir = "./posts/"
fn = note_list[idx].created.strftime('%Y-%m-%d-')+title_to_filename(note_list[idx].title)
f = open("{}{}".format(suffix_dir, fn), "wb")

from imgurpython import ImgurClient
import credentials

client_id = credentials.client_id
client_secret = credentials.client_secret

print("Login imgur")
client = ImgurClient(client_id, client_secret)

for image in note_list[idx].images():
    if image.exists():
        print("Upload {}".format(image.path))
        result = client.upload_from_path(image.path)
        
        data = data.replace("[image:{}]".format(image.path.split("/Note Images/")[1]), "<img src='{}' />".format(result['link']))
        print(result['link'])
    
f.write(data.encode('utf-8'))
f.close()

