class LetterTreeNode:
    def __init__(self, is_word):
        self.is_word = is_word
        self.children = dict()


class LetterTree:
    def __init__(self, words):
        """Given a list of words, will create a LetterTree that contains all the paths
        for all the given words"""

        #Sets the root node
        self.root = LetterTreeNode(False)

        #Iterates through the list of words
        for word in words:

            #At the beginning of each word, we reset the current_node back to the root
            current_node = self.root

            #Iterates through the list of letters in word
            for letter in word:

                #Determines if the children (values) of the current node (key) we are at, include the current letter
                if letter not in current_node.children.keys():
                    #If this letter is not in the current node's dictionary, then we add the letter to it's dictionary
                    #BUT, say the node is not a word (Meaning the path to this node does not spell a word)
                    current_node.children[letter] = LetterTreeNode(False)

                #Regardless if the current letter was already in the node's dictionary or not, we then shift the
                #current node to the current letter, then go to the next letter in the word
                current_node = current_node.children[letter]
            #Once we iterate through all the letters of the word, the path to the node of the  final letter
            #must be a word so we set it as such
            current_node.is_word = True

    def lookup(self, word):
        """"Iterates through a given word's letters and returns the node for the final
        letter in the node if it exists, or returns nothing if the tree doesn't contain a path
        that spells this word"""
        current_node = self.root
        for letter in word:
            if letter not in current_node.children.keys():
                return None
            current_node = current_node.children[letter]
        return current_node


    def is_word(self, word):
        """Returns true if the given word is in the LetterTree and the final letter of
        said word has a is_word value of True"""
        word_node = self.lookup(word)
        if word_node is None:
            return False
        return word_node.is_word

def basic_english():
    """Creates a LetterTree with the given list of words"""
    with open('basic_english_word_list.txt', 'rt') as file:
        words = []
        for line in file:
            word = line.strip().lower()
            words.append(word)
    return LetterTree(words)