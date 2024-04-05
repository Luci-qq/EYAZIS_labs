import nltk
import string
import pymorphy2

class TextHandler:
    def __init__(self):
        self.stop_words = nltk.corpus.stopwords.words('russian')
        self.bigram_measures = nltk.BigramAssocMeasures()
        self.morph_analyzer = pymorphy2.MorphAnalyzer()

    def tokenize(self, text):
        result = []
        words = nltk.word_tokenize(text)
        for word in words:
            if (word not in self.stop_words) and (word not in string.punctuation):
                result.append(word)
        return result

    def leksems(self, text):
        leksems = []
        words = self.tokenize(text)
        for word in words:
                leksems.append(self.morph_analyzer.parse(word)[0].normal_form)
        leksems.sort()
        return leksems

    def analyze(self, text):
        words = self.tokenize(text)
        finder = nltk.BigramCollocationFinder.from_words(
            words)
        finder.apply_freq_filter(1)
        tuple_list = finder.nbest(self.bigram_measures.pmi, 10)
        return list(list(t) for t in zip(*tuple_list))

