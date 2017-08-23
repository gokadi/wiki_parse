# wiki_parse
Wikipedia parser. Use NLTK, bs4 and Wikipedia

Inputs - article_name, content_level.
Content level in percentage. For example: text contains of 10 sentences, content_level = 50 -> summarized text contains of 5 sentences.
Script requests article with inputted name and parses it into the following structure:
```python
[
  [
    Title,
    Full text,
    Section/Subsection,
    Summarized text,
    Keywords of section text
  ],
  [{ second section/subsection list }],
  [...]
]
```
