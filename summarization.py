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
    for s in word_sent:
        for word in s:
            if word not in self.stopwords:
                freq[word] += 1
    # frequencies normalization and fitering
    for w in freq.keys():
        freq[w] /= len(freq)
    return freq

  def summarize(self, text, content_level):
    """
      Return a list of n sentences
      which represent the summary of text.
    """

    if len(text) != 0 and content_level < 100:
        sents = sent_tokenize(text)
        n = round(len(sents) * content_level / 100 + 0.5)
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
      freq = defaultdict(int)
      lmtzr = WordNetLemmatizer()
      if len(text) != 0:
          word_sent = word_tokenize(text)
          word_sent = [word.lower() for word in word_sent if word not in self.stopwords]
          word_sent = [lmtzr.lemmatize(word) for word in word_sent]
          for word in word_sent:
              if word not in self.stopwords and '\'' not in word and '`' not in word and word.lower() != 'the':
                  freq[word] += 1
          # frequencies normalization
          for w in freq.keys():
              freq[w] /= len(freq)
          all_keys = freq
          keys = dict(sorted(all_keys.items(), key=operator.itemgetter(1), reverse=True)[:5])
          return ', '.join(keys.keys())
      else:
          return ''

if __name__ == '__main__':
    fs= FrequencySummarizer()
    a = fs.summarize("I've tried ", 50)
    print('1 '+a)
    print(round(0.5+0.1))