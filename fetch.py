# fetch.py
# scrape the Texas Essential Knowledge and Skills
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

import urllib2
from bs4 import BeautifulSoup
import re
import json
import string


def format(text):
  text = re.sub(u'\u00a7', '', text)
  text = re.sub(u'\u00a0', '', text)
  text = re.sub('\n', '', text)  
  text = re.sub(' +', ' ', text)
  text = re.sub('[0-9][0-9][0-9][.][0-9][0-9][0-9]', '', text)
  text = re.sub('[0-9][0-9][0-9][.][0-9][0-9]', '', text)
  text = re.sub('[0-9][0-9][0-9][.][0-9]', '', text)
  text = re.sub('Beginning with School Year (.*)[.]?$', '', text)
  text = re.sub(r'[\(]One-Half to One Credit[\)]', '', text)
  text = re.sub(r'[\(]One-Half Credit to One Credit[\)]', '', text)
  text = re.sub(r'[\(]One-Half to Two Credits[\)]', '', text)
  text = re.sub(r'[\(]One-Half to Three Credits[\)]', '', text)
  text = re.sub(r'[\(]One to Three Credits[\)]', '', text)
  text = re.sub(r'[\(]One Credit[\)]', '', text)
  text = re.sub(r'[\(]Two Credits[\)]', '', text)
  text = re.sub(r'[\(]Elective Credit[\)]', '', text)
  text = re.sub(r'[\(]One-Half Credit[\)]', '', text)
  text = re.sub(r'[\(]One-Half Credit Per Semester[\)]', '', text)
  text = re.sub(r'[\(]One to Two Credits[\)]', '', text)
  text = re.sub(r'[\(]Two to Three Credits[\)]', '', text)
  text = re.sub(r'[\(]One-Half to One Science Credit[\)]', '', text)
  text = re.sub(r'[\(]One Science Credit[\)]', '', text)
  text = re.sub(r'[\(]One Physics Credit[\)]', '', text)
  text = re.sub(r'[\(]One Credit Per Level[\)]', '', text)
  text = re.sub(r'[\(]One to One and One-Half Credits[\)]', '', text)
  text = text.strip()
  text = text.rstrip(',')
  text = text.rstrip('.')
  text = text.lstrip('.')
  text = text.rstrip(';')
  
  return text.strip()


upper_letters = []
for letter in string.uppercase:
  upper_letters.append(letter)
for letter in string.uppercase:
  upper_letters.append(letter+letter)

data = {}

chapters = {
  '110' : 'English Language Arts and Reading', 
  '111' : 'Mathematics',
  '112' : 'Science', 
  '113' : 'Social Studies', 
  '114' : 'Languages Other Than English', 
  '115' : 'Health Education', 
  '116' : 'Physical Education', 
  '117' : 'Fine Arts',
  '118' : 'Economics with Emphasis on the Free Enterprise System and Its Benefits',
  '126' : 'Technology Applications', 
  '127' : 'Career Development',
  '128' : 'Spanish Language Arts and Reading and English as a Second Language',
  '130' : 'Career and Technical Education'
}

for chapter in chapters:
  chapter_id = chapter
  chapter_name = chapters[chapter]
  subchapter_data = {}
  urls = []
  if chapter == '130':
    subchapters = 'abcdefghijklmnopqrs'
  else:
    subchapters = 'abcdef' 
  for subchapter in subchapters:
    url = 'http://ritter.tea.state.tx.us/rules/tac/chapter%s/ch%s%s.html' % (chapter, chapter, subchapter)
    section_data = {}
    try:
      req = urllib2.Request(url)
      response = urllib2.urlopen(req)
      result = response.read()
      soup = BeautifulSoup(result)
    except:
      break

    for firstline in soup.find_all("p", class_="firstline"):      
      subchapter_pattern = re.compile('Subchapter %s. (.*)' % subchapter.upper(), re.DOTALL)
      for name in re.findall(subchapter_pattern, format(firstline.text)):
        subchapter_name = name

    for firstline in soup.find_all("p", class_="CHAPTERORSUBCHAPTE"):
      subchapter_pattern = re.compile('Subchapter %s. (.*)' % subchapter.upper(), re.DOTALL)
      for name in re.findall(subchapter_pattern, format(firstline.text)):
        subchapter_name = name



    for section in soup.find_all("p", class_="SECTIONHEADING"):
      #The name of this section can be fuond in the anchor tags immediate after the section heading p tag
      a =  section.find_next('a')
      section_id = a['name']  

      #Create an empty set of subsections
      sub_data = {}
      subsection_number = 0

      for subsection in section.find_next_siblings("p"):
        #For each subsection that comes after the most recent 'SECTIONHEADING' p tag
        if 'SUBSECTIONa' in subsection['class']: 
          #Create an empty set of paragraphs
          par_data = {}      
          par_number = 1        

          for paragraph in subsection.find_next_siblings("p"):
            #For each paragraph that comes after the most recent 'SUBSECTIONa' p tag
            if paragraph['class'][0] == 'PARAGRAPH1':
              #Create an empty set of subparagraphs
              sub_para = {}
              subpara_number = 0                       

              for subparagraph in paragraph.find_next_siblings("p"): 
                #For each subparagraph that comes after the most recent 'PARAGRAPH1' p tag               
                if subparagraph['class'][0] == 'SUBPARAGRAPHA':
                  #Create an empty set of clauses
                  clause_data = {}
                  clause_number = 0
                  for clause in subparagraph.find_next_siblings("p"):
                    #For each clause associated with the current subparagraph...
                    if clause['class'][0] == 'CLAUSEi':
                      #each clause is specified with a lowercase 'i'
                      romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv']
                      clause_data[romans[clause_number]] = [format(clause.text)]
                      clause_number += 1
                    elif clause['class'][0] in ['PARAGRAPH1', 'SUBSECTIONa', 'SUBPARAGRAPHA']:
                      #while iterating if we hit anything other than a clause tag, exit the loop
                      break

                  subpara_letter = upper_letters[subpara_number]
                  sub_para[subpara_letter] = [format(subparagraph.text), clause_data]
                  subpara_number += 1
                elif subparagraph['class'][0] in ['PARAGRAPH1', 'SUBSECTIONa']:
                  #While iterating, if we encounter a tag other than a subparagraph, we should exit the for loop
                  break
              #Append the title of the paragraph and all subparagraphs associated with that paragraph
              par_data[par_number] = [format(paragraph.text), sub_para] 
              par_number+=1
            elif paragraph['class'][0] == 'SUBSECTIONa':
              #While iterating, if we encounter a subsection tag (expecting 'PARAGRAH1') we have found the end of the current subsection
              break
          
          #Subsections are denoted with a lowercase alphabet (a,b,c,d, ... )
          subsection_letter = string.lowercase[subsection_number]
          #Append the title of the subsection and the associated paragraph data belonging to that subsection
          sub_data[subsection_letter] = [format(subsection.text), par_data]
          #Prepare for the next subsection
          subsection_number += 1

      #Append the subsection data to each section
      section_data[section_id] = [format(section.text), sub_data]

    #Append the section data to each subchapter
    subchapter_data[subchapter] = [subchapter_name, section_data]

  #Append the title of the section and all of the associated subsections belonging to that section 
  data[chapter] = ['%s' % chapter_name, subchapter_data]
    

with open('data.json', 'wb') as f:
  json.dump(data, f, sort_keys=True, indent = True)
f.closed
