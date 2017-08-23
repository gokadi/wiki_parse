import operator
from nltk.tokenize import sent_tokenize,word_tokenize
from collections import defaultdict
from string import punctuation
from heapq import nlargest
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


class FrequencySummarizer:

    def __init__(self):
        self.freq = dict()
        self.stopwords = set(stopwords.words('english') + list(punctuation))

    def compute_frequencies(self, word_sent):
        """
        Compute the frequency of each of word.
        :param word_sent: list of sentences already tokenized by words
        :return: dictionary {word: frequency}
        """
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self.stopwords:
                    freq[word] += 1
        for w in freq.keys():
            freq[w] /= len(freq)
        return freq

    def summarize(self, text, content_level):
        """
        Represent summary of the text
        :param text: text to be summarized
        :param content_level: percentage of output
        (100 - full text, 50 - half of the sentences).
        Used to count number of sentences to be output
        :return: list of n sentences which represent summary of the text
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
            print(ranking)
            sents_idx = self.rank(ranking, n)
            return " ".join(sents[j] for j in sents_idx)
        else:
            return text

    def rank(self, ranking, n):
        """
        Returns the first n sentences with highest ranking
        :param ranking: dict of sentences with their ranks {id: rank}
        :param n: number of sentences to be returned
        :return:
        """
        return nlargest(n, ranking, key=ranking.get)

    def keywords(self, text):
        """
        Return 5 most keywords
        :param text: text, which keywords need to be searched
        :return: string of 5 keywords, separated by commas
        """
        freq = defaultdict(int)
        lmtzr = WordNetLemmatizer()
        if len(text) != 0:
            word_sent = word_tokenize(text)
            word_sent = [word.lower() for word in word_sent if word not in self.stopwords]
            word_sent = [lmtzr.lemmatize(word) for word in word_sent]
            for word in word_sent:
                if word not in self.stopwords and '\'' not in word and '`' not in word and word.lower() != 'the':
                    freq[word] += 1
            for w in freq.keys():
                freq[w] /= len(freq)
            all_keys = freq
            keys = dict(sorted(all_keys.items(), key=operator.itemgetter(1), reverse=True)[:5])
            return ', '.join(keys.keys())
        else:
            return ''

if __name__ == '__main__':
    fs= FrequencySummarizer()
    a = fs.summarize("I've tried.I've tried.I've tried. I've tried. ", 50)
    print('1 '+a)
    print(round(0.5+0.1))