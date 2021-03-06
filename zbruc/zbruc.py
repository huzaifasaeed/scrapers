#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from bs4 import BeautifulSoup
import codecs
import re
import csv
from transliterate import translit

def process_file(filename, fout_csv, author):
    print("processing %s" % filename)
    csvwriter = csv.writer(fout_csv)
    with open(filename, 'r') as fin:
        soup = BeautifulSoup(fin, 'html.parser')
    title_elt = soup.find("div", id="page-title")
    title = title_elt.text.strip()
    if title[-1] == '.': title = title[:-1]
    # find pubishing info in a crappy way
    p_elts = soup.find_all("p")
    publish_text = ""
    for p_elt in p_elts:
        p_text = p_elt.text
        if len(p_text) > 2 and p_text[0] == '[' and p_text[-1] == ']':
            publish_text = p_text[1:-1]
            break
    content_elt = soup.find("div", id="content")
    full_text = content_elt.text
    out_file_name = translit(author, 'uk', reversed=True) + "/" + translit(title, 'uk', reversed=True) + ".txt"
    csvwriter.writerow([author, out_file_name, title, publish_text, len(full_text)])
    with open(out_file_name, "w") as fout:
        fout.write(full_text)


if __name__ == "__main__":
    author_translit = translit(sys.argv[2], "uk", reversed=True)
    os.mkdir(author_translit)
    with open(sys.argv[1], 'r') as fin, open(author_translit + ".csv", 'w') as fout:
        for filename in map(str.rstrip, fin):
            process_file(filename, fout, sys.argv[2])
