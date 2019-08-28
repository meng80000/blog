#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup

def xss(old_content):
    valid_tag = {
        "p": ["class", "id"],
        "img": ["src"],
        "div": ["class"]
    }
    soup = BeautifulSoup(old_content, "html.parser")
    tags = soup.find_all()
    for tag in tags:
        if tag.name not in valid_tag:
            tag.decompose()
        if tag.attrs:
            for k in list(tag.attrs.keys()):
                if k not in valid_tag[tag.name]:
                    del tag.attrs[k]
    new_content = soup.decode()
    return new_content