import wikipedia
import json
from bs4 import BeautifulSoup
from summarization import FrequencySummarizer
import sys
import time
start = time.time()
try:
    article_name = sys.argv.get[2]
except AttributeError:
    article_name = "Michael Jackson"
try:
    content_level = int(sys.argv.get[3])
except AttributeError:
    content_level = 100
article = wikipedia.page(article_name)
# In case of multiple possible articles upper line throws 'wikipedia.DisambiguationError'
wiki_sect_subsect = [BeautifulSoup(s, 'lxml').get_text() for s in article.sections]
import requests
response = requests.get(article.url)
soup = BeautifulSoup(response.content, 'lxml')


get_section = lambda h: h.get_text().replace('[edit]', '')
# We need below to differ sections from subsections
soup_sect = [get_section(h2) for h2 in soup.findAll('h2')
             if get_section(h2) != 'Contents']
soup_subsect = [get_section(h3) for h3 in soup.findAll('h3')
                if get_section(h3) != 'Contents']
soup_subsubsect = [get_section(h4) for h4 in soup.findAll('h4')
                if get_section(h4) != 'Contents']
p_article = list()
for sect_name in wiki_sect_subsect:
    ins_list = list()
    ins_list.append(sect_name)  # Title of section/subsection
    ins_list.append(article.section(sect_name))  # Text of section/subsection

    if sect_name in soup_sect:  # Indicator
        ins_list.append('Section')
    elif sect_name in soup_subsect:
        ins_list.append('Subsection')
    elif sect_name in soup_subsubsect:
        ins_list.append('Subsection')
    else:
        ins_list.append('ERROR. No section %s' % sect_name)

    fs = FrequencySummarizer()
    ins_list.append(fs.summarize(ins_list[1], content_level))  # Summarizing
    ins_list.append(fs.keywords(ins_list[1]))  # Keywords
    p_article.append(ins_list)

p_article = json.dumps(p_article, indent=2, ensure_ascii=False)
# with open('first_try.txt', 'w', encoding='utf-8') as file:
#     file.write(p_article)
print(p_article.encode('utf-8'))
