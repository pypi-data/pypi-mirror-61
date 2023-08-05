#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile
import pathlib

import urllib.request

from itertools import permutations


OXFORD_URL = "https://www.lexico.com/en/definition"
ALTERNATE_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

dict_path = "/usr/share/dict/american-english"


def download(url):
    tmp = tempfile.gettempdir()
    data_dir = os.path.join(tmp, ".crossword-solver")

    dest_file = os.path.join(data_dir, "words.txt")
    if pathlib.Path(dest_file).is_file():
        print(f"File exists at {dest_file}")
        return dest_file

    os.makedirs(data_dir, exist_ok=True)
    with urllib.request.urlopen(url) as response:
        with open(dest_file, "wb") as f:
            shutil.copyfileobj(response, f)

    return dest_file


def main():
    try:
        with open(dict_path) as f:
            eng_words = set(i.strip() for i in f.readlines())
    except IOError:
        print(
            f"{dict_path} does not exits, consider to install on Ubuntu using `apt install wamerican`"
        )
        print(f"Downloading {ALTERNATE_URL} for list of words...")
        try:
            local_location = download(ALTERNATE_URL)
            print(f"Downloaded to {local_location}")
            with open(local_location) as f:
                eng_words = set(i.strip() for i in f.readlines())
        except Exception as e:
            print(f"Failed to get list of words, error: {e}. Good luck!")

    if len(sys.argv) != 2:
        exit("Please enter characters, e.g: carono")

    found = set()
    for chars in permutations(sys.argv[1].lower().strip()):
        word = "".join(chars)
        if word in eng_words:
            found.add(word)

    if found:
        for word in found:
            print(f"{word}: {OXFORD_URL}/{word}")
    else:
        print("Word not found")


if __name__ == "__main__":
    main()
