# g2p ID: Indonesian Grapheme-to-Phoneme Converter

This library is developed to convert Indonesian (Bahasa Indonesia) graphemes (words) to phonemes in IPA. We followed the methods and designs used in the English equivalent library, [g2p](https://github.com/Kyubyong/g2p).

## Installation

```bash
pip install git+https://github.com/bookbot-kids/g2p_id.git
```

## How to Use

```py
from g2p_id import G2p

texts = [
    "Ia menyayangi yang lain.",
    "Mereka sedang bermain bola di lapangan.",
    "Hey kamu yang di sana!",
    "Saya sedang memerah susu sapi.",
]

g2p = G2p()
for text in texts:
    print(g2p(text))

>> ['ia', ' ', 'məɲajaŋi', ' ', 'jaŋ', ' ', 'lain', ' ', '.']
>> ['məreka', ' ', 'sədaŋ', ' ', 'bərmain', ' ', 'bola', ' ', 'di', ' ', 'lapaŋan', ' ', '.']
>> ['hej', ' ', 'kamu', ' ', 'jaŋ', ' ', 'di', ' ', 'sana', ' ', '!']
>> ['saja', ' ', 'sədaŋ', ' ', 'məmərah', ' ', 'susu', ' ', 'sapi', ' ', '.']
```

## Algorithm

This is heavily inspired from the English [g2p](https://github.com/Kyubyong/g2p).

1. Spells out arabic numbers and some currency symbols, e.g. `Rp 200,000 -> dua ratus ribu rupiah`. This is borrowed from [Cahya's code](https://github.com/cahya-wirawan/text_processor).
2. Attempts to retrieve the correct pronunciation for heteronyms based on their [POS (part-of-speech) tags](#pos-tagging).
3. Looks up a lexicon (pronunciation dictionary) for non-homographs. This list is originally from [ipa-dict](https://github.com/open-dict-data/ipa-dict/blob/master/data/ma.txt), and we later made a [modified version](https://huggingface.co/datasets/bookbot/id_word2phoneme).
4. For OOVs, we predict their pronunciations using either a [BERT model](https://huggingface.co/bookbot/id-g2p-bert) or an [LSTM model](https://huggingface.co/bookbot/id-g2p-lstm).

## Phoneme and Grapheme Sets

We followed the IPA convention provided in the original [ipa-dict](https://github.com/open-dict-data/ipa-dict/blob/master/data/ma.txt). The list of grapheme and phoneme characters are as the following:

```python
graphemes = ["'", '-', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
phonemes = ['-', 'a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'z', 'ŋ', 'ə', 'ɲ', 'ʃ', 'ʒ', 'ʔ']
```

## Notes

### Homographs

Indonesian words (as far as we know) only have one case of homograph, that is, differing ways to pronounce the letter `e`. For instance, in the word `apel` (meaning: apple), the letter `e` is a mid central vowel `ə`. On the other hand, the letter `e` in the word `apel` (meaning: going to a significant other's house; courting), is a closed-mid front unrounded vowel `e`. Sometimes, a word might have >1 `e`s pronounced in both ways, for instance, `mereka` (meaning: they) is pronounced as `məreka`. Because of this, there needs a way to disambiguate homographs, and in our case, we used their POS (part-of-speech) tags. However, this is not a foolproof method since homographs may even have the same POS tag. We are considering a contextual model to handle this better.

### OOV Prediction

Initially, we relied on a sequence2sequence LSTM model for OOV (out-of-vocabulary) prediction. This was a natural choice given that it can "automatically" learn the rules of grapheme-to-phoneme conversion without having to determine the rules by hand. However, we soon noticed that despite its validation results, the model performed poorly on unseen words, especially on longer ones. We needed a more controllable model that makes predictions on necessary characters only. We ended up with a customized BERT that predicts the correct pronunciation of the letter `e` while keeping the rest of the string unchanged. We then apply a hand-written g2p conversion algorithm that handles the other characters.

<!-- You can find more detail in [this blog post](). -->

### POS Tagging

We trained an [NLTK PerceptronTagger](https://www.nltk.org/_modules/nltk/tag/perceptron.html) on the [POSP](https://huggingface.co/datasets/indonlu) dataset, which achieved 0.956 and 0.945 F1-score on the valid and test sets, respectively. Given its performance and speed, we decided to adopt this model as the POS tagger for the purpose of disambiguating homographs, which is just like the English g2p library.

<details>
  <summary>Validation Results</summary>

    | tag       | precision | recall   | f1-score |
    | --------- | --------- | -------- | -------- |
    | B-$$$     | 1.000000  | 1.000000 | 1.000000 |
    | B-ADJ     | 0.904132  | 0.864139 | 0.883683 |
    | B-ADK     | 1.000000  | 0.986667 | 0.993289 |
    | B-ADV     | 0.966874  | 0.976987 | 0.971904 |
    | B-ART     | 0.988920  | 0.978082 | 0.983471 |
    | B-CCN     | 0.997934  | 0.997934 | 0.997934 |
    | B-CSN     | 0.986395  | 0.963455 | 0.974790 |
    | B-INT     | 1.000000  | 1.000000 | 1.000000 |
    | B-KUA     | 0.976744  | 0.976744 | 0.976744 |
    | B-NEG     | 0.992857  | 0.972028 | 0.982332 |
    | B-NNO     | 0.919917  | 0.941288 | 0.930480 |
    | B-NNP     | 0.917685  | 0.914703 | 0.916192 |
    | B-NUM     | 0.997358  | 0.954488 | 0.975452 |
    | B-PAR     | 1.000000  | 0.851064 | 0.919540 |
    | B-PPO     | 0.991206  | 0.991829 | 0.991517 |
    | B-PRI     | 1.000000  | 0.928571 | 0.962963 |
    | B-PRK     | 0.793103  | 0.851852 | 0.821429 |
    | B-PRN     | 0.988327  | 0.988327 | 0.988327 |
    | B-PRR     | 0.995465  | 1.000000 | 0.997727 |
    | B-SYM     | 0.999662  | 0.999323 | 0.999492 |
    | B-UNS     | 0.916667  | 0.733333 | 0.814815 |
    | B-VBE     | 1.000000  | 0.985714 | 0.992806 |
    | B-VBI     | 0.929119  | 0.877034 | 0.902326 |
    | B-VBL     | 1.000000  | 1.000000 | 1.000000 |
    | B-VBP     | 0.926606  | 0.933457 | 0.930018 |
    | B-VBT     | 0.939759  | 0.953333 | 0.946498 |
    | --------- | --------- | -------- | -------- |
    | macro avg | 0.966490  | 0.946937 | 0.955913 |

</details>

### Attempts that Failed

- Parsed [online PDF KBBI](https://oldi.lipi.go.id/public/Kamus%20Indonesia.pdf), but it turns out that it has very little phoneme descriptions.
- Scraped [online Web KBBI](https://github.com/laymonage/kbbi-python), but it had a daily bandwidth which was too low to be used at this level.

### Potential Improvements

There is a ton of room for improvements, both from the technical and the linguistic side of the approaches. Consider that a failure of one component may cascade to an incorrect conclusion. For instance, an incorrect POS tag can lead to the wrong phoneme, ditto for incorrect BERT/LSTM prediction. We propose the following future improvements.

- [ ] Use a larger pronunciation lexicon instead of having to guess.
- [x] Find a larger homograph list.
- [x] Use contextual model instead of character-level RNNs.
- [x] Consider hand-written rules for g2p conversion.
- [ ] Add to PyPI.

## References

```
@misc{g2pE2019,
  author = {Park, Kyubyong & Kim, Jongseok},
  title = {g2pE},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/Kyubyong/g2p}}
}
```

```
@misc{TextProcessor2021,
  author = {Cahya Wirawan},
  title = {Text Processor},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/cahya-wirawan/text_processor}}
}
```

## Contributors

<a href="https://github.com/w11wo/g2p_id/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=w11wo/g2p_id" />
</a>
