from teks import teks

#Print out every substandard

for chapter in teks.chapters:
  for subchapter in chapter.subchapters:
    for section in subchapter.sections:
      for domain in section.domains:
        for standard in domain.standards:
          for substandard in standard.substandards:
            print substandard.title.encode('ascii', 'ignore')

