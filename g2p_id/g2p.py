"""
Copyright 2022 [PT BOOKBOT INDONESIA](https://bookbot.id/)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import re
from typing import Dict, List, Tuple
import unicodedata
from builtins import str as unicode
import nltk
from nltk.tag.perceptron import PerceptronTagger
from nltk.tokenize import word_tokenize


try:
    word_tokenize("")
except LookupError:
    nltk.download("punkt")

from g2p_id.text_processor import TextProcessor
from g2p_id.lstm import LSTM
from g2p_id.bert import BERT

resources_path = os.path.join(os.path.dirname(__file__), "resources")


def construct_homographs_dictionary() -> Dict[str, Tuple[str, str, str, str]]:
    """Creates a dictionary of homographs

    Returns:
        Dict[str, Tuple[str, str, str, str]]: 
            Key: WORD
            Value: (PH1, PH2, POS1, POS2)
    """
    homograph_path = os.path.join(resources_path, "homographs_id.tsv")
    homograph2features = dict()
    with open(homograph_path, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            grapheme, phone_1, phone_2, pos_1, pos_2 = line.strip("\n").split("\t")
            homograph2features[grapheme.lower()] = (phone_1, phone_2, pos_1, pos_2)

    return homograph2features


def construct_lexicon_dictionary() -> Dict[str, str]:
    """Creates a lexicon dictionary.

    Returns:
        Dict[str, str]:
            Key: WORD
            Value: Phoneme (IPA)
    """
    lexicon_path = os.path.join(resources_path, "lexicon_id.tsv")
    lexicon2features = dict()
    with open(lexicon_path, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            grapheme, phoneme = line.strip("\n").split("\t")
            lexicon2features[grapheme.lower()] = phoneme
    return lexicon2features


class G2p:
    def __init__(self, model_type="BERT"):
        """Constructor for G2p.

        Args:
            model_type (str, optional): 
                Type of neural network to use for prediction. 
                Choices are "LSTM" or "BERT". Defaults to "BERT".
        """
        self.homograph2features = construct_homographs_dictionary()
        self.lexicon2features = construct_lexicon_dictionary()
        self.normalizer = TextProcessor()
        self.tagger = PerceptronTagger(load=False)
        tagger_path = os.path.join(resources_path, "id_posp_tagger.pickle")
        self.tagger.load("file://" + tagger_path)
        self.model = BERT() if model_type == "BERT" else LSTM()
        self.pos_dict = {
            "N": ["B-NNO", "B-NNP", "B-PRN", "B-PRN", "B-PRK"],
            "V": ["B-VBI", "B-VBT", "B-VBP", "B-VBL", "B-VBE"],
            "A": ["B-ADJ"],
            "P": ["B-PAR"],
        }

    def _preprocess(self, text: str) -> str:
        """Performs preprocessing.
        (1) Adds spaces in between tokens
        (2) Normalizes unicode and accents
        (3) Normalizes numbers
        (4) Lower case texts
        (5) Removes unwanted tokens

        Arguments:
            text (str): Text to preprocess.

        Returns:
            str: Preprocessed text.
        """
        text = " ".join(word_tokenize(text))
        text = unicode(text)
        text = "".join(
            char
            for char in unicodedata.normalize("NFD", text)
            if unicodedata.category(char) != "Mn"
        )
        text = self.normalizer.normalize(text).strip()
        text = text.lower()
        text = re.sub("[^ a-z'.,?!\-]", "", text)
        return text

    def _rule_based_g2p(self, text: str) -> str:
        """Applies rule-based Indonesian grapheme2phoneme conversion.

        Args:
            text (str): Grapheme text to convert to phoneme.

        Returns:
            str: Phoneme string.
        """
        _PHONETIC_MAPPING = {
            "ny": "ɲ",
            "ng": "ŋ",
            "c": "tʃ",
            "'": "ʔ",
            "aa": "aʔa",
            "ii": "iʔi",
            "oo": "oʔo",
            "əə": "əʔə",
            "j": "dʒ",
            "y": "j",
            "q": "k",
            "x": "ks"
        }

        _CONSONANTS = "bdfghjklmnprstvwɲ"

        if text.endswith("k"):
            text = text[:-1] + "ʔ"

        for g, p in _PHONETIC_MAPPING.items():
            text = text.replace(g, p)

        for c in _CONSONANTS:
            text = text.replace(f"k{c}", f"ʔ{c}")

        return text

    def __call__(self, text: str) -> List[str]:
        """Grapheme-to-phoneme converter.

        1. Preprocess and normalize text
        2. Word tokenizes text
        3. Predict POS for every word
        4. If word is non-alphabetic, add to list (i.e. punctuation)
        5. If word is a homograph, check POS and use matching word's phonemes
        6. If word is a non-homograph, lookup lexicon
        7. Otherwise, predict with a neural network

        Args:
            text (str): Grapheme text to convert to phoneme.

        Returns:
            List[str]: List of strings in phonemes.
        """
        text = self._preprocess(text)
        words = word_tokenize(text)
        tokens = self.tagger.tag(words)

        prons = []
        for word, pos in tokens:
            pron = ""
            if re.search("[a-z]", word) is None:  # non-alphabetic
                pron = word

            elif word in self.homograph2features:  # check if homograph
                pron1, pron2, pos1, _ = self.homograph2features[word]

                # check for the matching POS
                if pos in self.pos_dict[pos1]:
                    pron = pron1
                else:
                    pron = pron2

            elif word in self.lexicon2features:  # non-homographs
                pron = self.lexicon2features[word]

            else:  # predict for OOV
                pron = self.model.predict(word)
                if isinstance(self.model, BERT):
                    pron = self._rule_based_g2p(pron)

            prons.append(pron)
            prons.append(" ")

        return prons[:-1]


def main():
    texts = [
        "Ia menyayangi yang lain.",
        "Mereka sedang bermain bola di lapangan.",
        "Hey kamu yang di sana!",
        "Rahel pergi ke sekolah dan bertemu dengan Budi.",
    ]
    g2p = G2p(model_type="BERT")
    for text in texts:
        print(g2p(text))


if __name__ == "__main__":
    main()
