import numpy as np
import re
import unicodedata
from builtins import str as unicode
from nltk.tag.perceptron import PerceptronTagger
from nltk.tokenize import word_tokenize

HOMOGRAPH_PATH = "g2p_id\homographs_id.tsv"
LEXICON_PATH = "g2p_id\lexicon_id.tsv"
POS_TAGGER_MODEL = "g2p_id\id_posp_tagger.pickle"


def construct_homographs_dictionary():
    homograph2features = dict()
    with open(HOMOGRAPH_PATH, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            grapheme, phone_1, phone_2, pos_1, pos_2 = line.strip("\n").split("\t")
            homograph2features[grapheme.lower()] = (phone_1, phone_2, pos_1, pos_2)

    return homograph2features


def construct_lexicon_dictionary():
    lexicon2features = dict()
    with open(LEXICON_PATH, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            grapheme, phoneme = line.strip("\n").split("\t")
            lexicon2features[grapheme.lower()] = phoneme
    return lexicon2features


class G2p(object):
    def __init__(self):
        super().__init__()
        self.homograph2features = construct_homographs_dictionary()
        self.lexicon2features = construct_lexicon_dictionary()
        self.tagger = PerceptronTagger(load=False)
        self.tagger.load(POS_TAGGER_MODEL)
        self.pos_dict = {
            "N": ["B-NNO", "B-NNP", "B-PRN", "B-PRN", "B-PRK"],
            "V": ["B-VBI", "B-VBT", "B-VBP", "B-VBL", "B-VBE"],
            "A": ["B-ADJ"],
            "P": ["B-PAR"],
        }

    def __call__(self, text):
        # preprocessing
        text = unicode(text)
        # text = normalize_numbers(text)
        text = "".join(
            char
            for char in unicodedata.normalize("NFD", text)
            if unicodedata.category(char) != "Mn"
        )
        text = text.lower()
        text = re.sub("[^ a-z'.,?!\-]", "", text)
        # text = text.replace("i.e.", "that is")
        # text = text.replace("e.g.", "for example")

        # # tokenization
        words = word_tokenize(text)
        tokens = self.tagger.tag(words)  # tuples of (word, tag)

        # steps
        prons = []
        for word, pos in tokens:
            pron = ""
            if re.search("[a-z]", word) is None:
                pron = word

            elif word in self.homograph2features:  # Check homograph
                pron1, pron2, pos1, pos2 = self.homograph2features[word]
                if pos in self.pos_dict[pos1]:
                    pron = pron1
                else:
                    pron = pron2
            elif word in self.lexicon2features.keys():  # lookup CMU dict
                pron = self.lexicon2features[word]

            else:  # predict for oov
                pron = word
            prons.append(pron)
            # prons.append(" ")

        return prons


g2p = G2p()
print(g2p("Nama saya Ananto, saya suka bermain bola."))
