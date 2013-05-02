# teks.py
# Scrape the data.json file produced from fetch.py and generate usable TEKS classes
# access the classes with: `from teks import teks`
#
# MIT License:
# Copyright (C) 2013 Quentin Donnellan
# http://qdonnellan.appspot.com
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json

with open('data.json', 'rb') as f:
  json_data = json.load(f)
f.closed

def makeSort(list_of_classes):
  return sorted(list_of_classes, key=lambda x: x.title)

class teksTop():
  def __init__(self, data):
    chapters = []
    for chapter in data:      
      chapters.append(teksChapter(data[chapter], chapter))
    self.chapters = makeSort(chapters)

class teksChapter():
  def __init__(self, data, key):
    subchapters = []
    self.title = data[0]
    self.id = key
    for subchapter in data[1]:
      subchapters.append(teksSubchapter(data[1][subchapter], subchapter))
    self.subchapters = makeSort(subchapters)

class teksSubchapter():
  def __init__(self, data, key):
    sections = []
    self.title = data[0]
    self.id = key
    for section in data[1]:
      sections.append(teksSection(data[1][section], section))
    self.sections = makeSort(sections)

class teksSection():
  def __init__(self, data, key):
    domains = []
    self.title = data[0]
    self.id = key
    for domain in data[1]:
      domains.append(teksDomain(data[1][domain], domain))
    self.domains = makeSort(domains)

class teksDomain():
  def __init__(self, data, key):
    standards = []
    self.title = data[0]
    self.id = key
    for standard in data[1]:
      standards.append(teksStandard(data[1][standard], standard))
    self.standards = makeSort(standards)

class teksStandard():
  def __init__(self, data, key):
    substandards = []
    self.title = data[0]
    self.id = key
    for substandard in data[1]:
      substandards.append(teksSubStandard(data[1][substandard], substandard))
    self.substandards = makeSort(substandards)

class teksSubStandard():
  def __init__(self, data, key):
    clauses = []
    self.title = data[0]
    self.id = key
    for clause in data[1]:
      clauses.append(teksClause(data[1][clause], clause))
    self.clauses = makeSort(clauses)

class teksClause():
  def __init__(self, data, key):
    self.title = data[0]
    self.id = key

teks = teksTop(json_data)
