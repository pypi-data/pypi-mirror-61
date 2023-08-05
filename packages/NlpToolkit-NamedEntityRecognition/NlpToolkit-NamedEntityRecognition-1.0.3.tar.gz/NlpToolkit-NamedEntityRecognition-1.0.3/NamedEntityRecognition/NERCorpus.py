from Corpus.Corpus import Corpus

from NamedEntityRecognition.NamedEntitySentence import NamedEntitySentence


class NERCorpus(Corpus):

    """
    Another constructor of NERCorpus which takes a fileName of the corpus as an input, reads the
    corpus from that file.

    PARAMETERS
    ----------
    fileName : str
        Name of the corpus file.
    """
    def __init__(self, fileName=None):
        super().__init__()
        if fileName is not None:
            inputFile = open(fileName, "r", encoding="utf8")
            lines = inputFile.readlines()
            for line in lines:
                self.addSentence(NamedEntitySentence(line))

    """
    addSentence adds a new sentence to the sentences list

    PARAMETERS
    ----------
    s : Sentence
        Sentence to be added.
    """
    def addSentence(self, s: NamedEntitySentence):
        self.sentences.append(s)
