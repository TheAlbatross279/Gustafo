from nltk.corpus import stopwords
from filter import Filter

class StopWordFilter(Filter):
    def filter(self, msg):
        return self.remove_stopwords(msg)

    def remove_stopwords(self, msg):
        filtered_msg = []
        for word in msg:
            if word not in stopwords.words('english'):
                filtered_msg.append(word)

        return filtered_msg

if __name__ == "__main__":
    s = StopWordFilter()
    f = s.filter(["my", "the", "hello"])
    print f
