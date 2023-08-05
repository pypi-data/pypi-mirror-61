class Gazetteer:

    __data: set
    __name: str

    """
    A constructor for a specific gazetteer. The constructor takes name of the gazetteer and file name of the
    gazetteer as input, reads the gazetteer from the input file.

    PARAMETERS
    ----------
    name : str
        Name of the gazetteer. This name will be used in programming to separate different gazetteers.
    fileName : str
        File name of the gazetteer data.
    """
    def __init__(self, name: str, fileName: str):
        self.__name = name
        self.__data = set()
        inputFile = open(fileName, "r", encoding="utf8")
        lines = inputFile.readlines()
        for line in lines:
            self.__data.add(line)

    """
    Accessor method for the name of the gazetteer.

    RETURNS
    -------
    str
        Name of the gazetteer.
    """
    def getName(self) -> str:
        return self.__name

    """
    The most important method in Gazetteer class. Checks if the given word exists in the gazetteer. The check
    is done in lowercase form.

    PARAMETERS
    ----------
    word : str
        Word to be search in Gazetteer.

    RETURNS
    -------
    bool
        True if the word is in the Gazetteer, False otherwise.
    """
    def contains(self, word: str) -> bool:
        return word.lower() in self.__data
