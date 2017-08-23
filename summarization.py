# coding=utf-8
"""
A summarizer based on the algorithm found in Classifier4J by Nick Lothan.
In order to summarize a document this algorithm first determines the
frequencies of the words in the document.  It then splits the document
into a series of sentences.  Then it creates a summary by including the
first sentence that includes each of the most frequent words.  Finally
summary's sentences are reordered to reflect that of those in the original
document.
"""
import operator

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


class FrequencySummarizer:

  def __init__(self):
    """
     Initialize the text summarizer.
     Words that have a frequency term lower than min_cut
     or higher than max_cut will be ignored.
    """
    self.freq = dict()
    self.stopwords = set(stopwords.words('english') + list(punctuation))

  def compute_frequencies(self, word_sent):
    """
      Compute the frequency of each of word.
      Input:
       word_sent, a list of sentences already tokenized.
      Output:
       freq, a dictionary where freq[w] is the frequency of w.
    """
    freq = defaultdict(int)
    lmtzr = WordNetLemmatizer()
    try:
        word_sent = [word for word in word_sent if word not in self.stopwords]
    except Exception:
        print(word_sent)
        raise Exception
    word_sent = [lmtzr.lemmatize(word) for word in word_sent]
    for word in word_sent:
        if word not in self.stopwords and '\'' not in word and '`' not in word and word.lower() != 'the':
          freq[word] += 1
    # frequencies normalization
    m = float(max(freq.values()))
    for w in freq.keys():
      freq[w] /= len(freq)
    return freq

  def summarize(self, text, content_level):
    """
      Return a list of n sentences
      which represent the summary of text.
    """
    sents = sent_tokenize(text)
    if len(sents) != 0 and content_level < 100:
        n = len(sents) * content_level // 100
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self.freq = self.compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self.freq:
                    ranking[i] += self.freq[w]
        sents_idx = self.rank(ranking, n)
        return " ".join(sents[j] for j in sents_idx)
    else:
        return text

  def rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)

  def keywords(self, text):
      # print(self.stopwords)
      if len(text) > 0:
          all_keys = self.compute_frequencies(word_tokenize(text))
          keys = dict(sorted(all_keys.items(), key=operator.itemgetter(1), reverse=True)[:5])
          return ', '.join(keys.keys())
      else:
          return ''

if __name__ == '__main__':
    fs= FrequencySummarizer()
    a = fs.keywords("I've tried PorterStemmer and Snowball but both don't work on all words, "
                "missing some very common ones. My test words are: \"cats running ran "
                "cactus cactuses cacti community communities\", and both get less than half right.")
    print(a)