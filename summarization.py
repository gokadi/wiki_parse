import operator

import nltk
from nltk.tokenize import sent_tokenize,word_tokenize
from collections import defaultdict
from string import punctuation
from heapq import nlargest
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


class FrequencySummarizer:

    def __init__(self):
        self.freq = dict()
        try:
            self.stopwords = set(stopwords.words('english') +
                                 list(punctuation) +
                                 list(['the', '`', '\'s', '\'re', '\'m'])
                                 )
        except LookupError:
            # In case of first run (only in Linux systems probably),
            # we need to download additional NLTK packages
            nltk.download('wordnet')
            nltk.download('punkt')
            nltk.download('stopwords')
            self.stopwords = set(stopwords.words('english') +
                                 list(punctuation) +
                                 list(['the', '`', '\'s', '\'re', '\'m'])
                                 )

    def compute_frequencies(self, word_sentences):
        """
        Compute the frequency of each of word.
        :param word_sentences: list of sentences tokenized by words
        :return: dictionary {word: frequency}
        """
        freq = defaultdict(int)  # defaultdict(int) let assign values to unexisting for the time being keys
        for s in word_sentences:  # for each sentence
            for word in s:  # for each word
                if word not in self.stopwords and len(word) > 1:  # if word not in stopwords
                    freq[word] += 1  # add 1 to number of word in freq dict
        for w in freq.keys():  # for each word in frequency dict
            freq[w] /= len(freq)  # count frequency
        return freq

    def summarize(self, text, content_level):
        """
        Represent summary of the text
        :param text: text to be summarized
        :param content_level: percentage of output (0-100)
        (100 - full text, 50 - half of the sentences).
        Used to count number of sentences to be output
        :return: list of n sentences which represent summary of the text
        """
        if not isinstance(text, str):
            raise Exception('Text for summarizing must be a string')
        if content_level <= 0:
            return ''
        elif len(text) != 0 and content_level < 100:  # if content-level = 100 no need to compute everything

            sents = sent_tokenize(text)  # Get list of sentences
            n = round(len(sents) * content_level / 100 + 0.5)  # Get amount of needed sentences for output
            word_sentences = [word_tokenize(s.lower()) for s in sents]  # List([words, for each sentence][...]...)

            self.freq = self.compute_frequencies(word_sentences)  # Get dictionary {word: frequency}

            ranking = defaultdict(int)  # defaultdict(int) let assign values to unexisting for the time being keys
            for i, sent in enumerate(word_sentences):  # sent - list of words for one sentence, i - sentence's index
                for w in sent:  # for each word in sentence
                    if w in self.freq:  # if words wasn't cleared in case of being a stop-word or something else
                        ranking[i] += self.freq[w]  # summarize word frequency
            top_ranked_sents = self.rank(ranking, n)  # returns n top (by frequency) sentences of the text

            return " ".join(sents[j] for j in top_ranked_sents)
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
        if not isinstance(text, str):
            raise Exception('Text for keywords search must be a string')
        all_keys = defaultdict(int)
        lmtzr = WordNetLemmatizer()
        if len(text) != 0:
            # split text in the list of words
            word_sentences = word_tokenize(text.replace('/', ' ')  # for situations like 'section/subsection'
                                           .replace('\'s', ' is')
                                           .replace('\'re', ' are')
                                           .replace('\'m', ' am')
                                           .replace('n\'t', ' not')
                                           .replace('-', '')
                                           .replace('–', ''))  # these two for dates (e.g. 1999-2019)
            # some preparations
            word_sentences = [word.lower() for word in word_sentences
                              if word not in self.stopwords and len(word) > 2]
            # lemmatize word (cats -> cat etc.)
            word_sentences = [lmtzr.lemmatize(word) for word in word_sentences]
            for word in word_sentences:  # for each word check again
                # note: there are two checks for stopwords in text, before lemmatization and after
                # this is needed, because some stopwords after lemmatize become something unreadable (like 'th' or 'h')
                # and also because of this we check for len(word) > 1 in first check
                if word not in self.stopwords \
                        and '`' not in word \
                        and '\'' not in word \
                        and '\"' not in word \
                        and not word.isdigit():
                    all_keys[word] += 1
            for w in all_keys.keys():
                all_keys[w] /= len(all_keys)
            keys = dict(sorted(all_keys.items(), key=operator.itemgetter(1), reverse=True)[:5])
            return ', '.join(keys)
        else:
            return ''
