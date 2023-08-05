from Corpus.Sentence import Sentence


class Paragraph:

    __sentences: list

    """
    A constructor of Paragraph class which creates a list sentences.
    """
    def __init__(self):
        self.__sentences = []

    """
    The addSentence method adds given sentence to sentences list.

    PARAMETERS
    ----------
    s : Sentence
        Sentence type input to add sentences.
    """
    def addSentence(self, s: Sentence):
        self.__sentences.append(s)

    """
    The sentenceCount method finds the size of the list sentences.

    RETURNS
    -------
    int
        The size of the list sentences.
    """
    def sentenceCount(self) -> int:
        return len(self.__sentences)

    """
    The getSentence method finds the sentence from sentences list at given index.

    PARAMETERS
    ----------
    index : int
        used to get a sentence.
        
    RETURNS
    -------
    Sentence
        sentence at given index.
    """
    def getSentence(self, index: int) -> Sentence:
        return self.__sentences[index]
