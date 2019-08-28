#!/usr/bin/env python
# -*- coding:utf-8 -*-


msg="""
<p id="a">
	床前明月光，
</p>
<p>
	疑是地上霜，
</p>
<p>
	举头望明月，
</p>
<script>alert(123)</script>
<p>
	底油思故乡。
</p>

"""
valid_tag={
    "p":["class","id"],
    "img":["src"],
    "div":["class"]
}
from bs4 import BeautifulSoup
soup=BeautifulSoup(msg,"html.parser")
tags=soup.find_all()
for tag in tags:
    if tag.name not in valid_tag:
        tag.decompose()
    if tag.attrs:
        for k in list(tag.attrs.keys()):
            if k not in valid_tag[tag.name]:
                del tag.attrs[k]

content_str=soup.decode()
print(content_str)