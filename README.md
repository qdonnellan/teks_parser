# Texas Essential Knowledge and Skills (TEKS) Parser
*Copyright (C) 2013 Quentin Donnellan*
*http://qdonnellan.appspot.com*

## What is this?
This is a python parser for the Texas Essential Knowledge and Skills (TEKS). It's function is quite simple: Read the HTML data from the TEKS websites, then turn it into useful json which can be iterated by your webapp. Feel free to download remix, etc. as I've attached an MIT license to this thing.

## How to use?

### Step 1: Run fetch.py
This script will scrape the various (and many) TEKS web-pages and spit out a structured JSON file containing every single TEKS object that currently exists. This takes several seconds (30 seconds is typical). You'll want to only do this once and then save that JSON is a useful place

### Step 2: Have fun!
Use the teks.py script if you want to push that JSON stuff into usable classes. Use the raw JSON if you want to iterate yourself.

### How to use teks.py
The TEKS are highly nested (it's actually insane) and here is how they do it:

-->Chapters-->Subchapters-->Sections-->Domains-->Standards-->SubStandards-->Clauses

Each level has an id and a title (which contains the text of that level)

If you wanted to iterate through all of the chapters and print out the title and id of each chapter, you would do something like:

    from teks import teks

    for chapter in teks.chapters:
      print chapter.id, chapter.title


### Not allergic to bitcoin
Whiskey donation fund: 1MraDxM8gywuiQeTNdMaLB7U4xhpUQ9YeJ