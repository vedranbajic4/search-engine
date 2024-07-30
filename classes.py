from colorama import Back, Style
import re


class Result(object):
    def __init__(self, index, weight):   # tekst je isecak, stranica je redni broj stranic
        self._tekst = ""
        self._weight = weight
        self._index = index

    def ispisi_rez(self, reci):   # fali hihglight
        if self._index >= 23:
            #pdf.cell(0, 10, f'Redni broj stranice: {self._index-22}', ln=True)
            print("Redni broj stranice: ", self._index-22)
        else:
            #pdf.cell(0, 10, f'Stranica nema redni broj (index: {self._index})', ln=True)
            print("Stranica nema redni broj (index: ", self._index, ")")


        for linija in self._tekst:
            #pdf.cell(0, 10, linija, ln=True)
            novi_tekst = re.split(r'[ ,\n]+', linija)
            for s in novi_tekst:
                if s.lower() in reci:
                    print(Back.YELLOW + s + Style.RESET_ALL, end=" ")
                else:
                    print(s, end=" ")
            print("")


        print("\n\n")

    def add_weight(self, v):
        self._weight += v

    def add_text(self, v):
        self._tekst = v

    def get_index(self):
        return self._index

    def get_weight(self):
        return self._weight

    # Comparison methods
    def __lt__(self, other):
        return self._weight > other._weight

    def __eq__(self, other):
        return self._weight == other._weight

    def postoji(self):
        return self._weight != 0


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word += 1

    def recursive(self, node):
        ret = 0
        for next in node.children.values():
            ret += self.recursive(next)

        return ret + node.is_end_of_word

    def search(self, word):     # vraca broj pojavljivanja reci na stranici (u trie-u)
        node = self.root
        for char in word:
            if char == '*':
                return self.recursive(node)

            if char not in node.children:
                return 0
            node = node.children[char]

        return node.is_end_of_word
