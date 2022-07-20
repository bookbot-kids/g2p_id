# g2p ID: Indonesian Grapheme-to-Phoneme Converter

This library is developed to convert Indonesian (Bahasa Indonesia) graphemes (words) to phonemes in IPA. We followed the methods and designs used in the English equivalent library, [g2p](https://github.com/Kyubyong/g2p).

## Installation

```bash
pip install g2p_id_py
```

## How to Use

```py
from g2p_id import G2p

texts = [
    "Apel itu berwarna merah.",
    "Rahel bersekolah di S M A Jakarta 17.",
    "Mereka sedang bermain bola di lapangan.",
]

g2p = G2p()
for text in texts:
    print(g2p(text))

>> [['a', 'p', 'ə', 'l'], ['i', 't', 'u'], ['b', 'ə', 'r', 'w', 'a', 'r', 'n', 'a'], ['m', 'e', 'r', 'a', 'h'], ['.']]
>> [['r', 'a', 'h', 'e', 'l'], ['b', 'ə', 'r', 's', 'ə', 'k', 'o', 'l', 'a', 'h'], ['d', 'i'], ['e', 's'], ['e', 'm'], ['a'], ['dʒ', 'a', 'k', 'a', 'r', 't', 'a'], ['t', 'u', 'dʒ', 'u', 'h'], ['b', 'ə', 'l', 'a', 's'], ['.']]
>> [['m', 'ə', 'r', 'e', 'k', 'a'], ['s', 'ə', 'd', 'a', 'ŋ'], ['b', 'ə', 'r', 'm', 'a', 'i', 'n'], ['b', 'o', 'l', 'a'], ['d', 'i'], ['l', 'a', 'p', 'a', 'ŋ', 'a', 'n'], ['.']]
```

## Algorithm

This is heavily inspired from the English [g2p](https://github.com/Kyubyong/g2p).

1. Spells out arabic numbers and some currency symbols, e.g. `Rp 200,000 -> dua ratus ribu rupiah`. This is borrowed from [Cahya's code](https://github.com/cahya-wirawan/text_processor).
2. Attempts to retrieve the correct pronunciation for homographs based on their [POS (part-of-speech) tags](#pos-tagging).
3. Looks up a lexicon (pronunciation dictionary) for non-homographs. This list is originally from [ipa-dict](https://github.com/open-dict-data/ipa-dict/blob/master/data/ma.txt), and we later made a modified version.
4. For OOVs, we predict their pronunciations using either a [BERT model](https://huggingface.co/bookbot/id-g2p-bert) or an [LSTM model](https://huggingface.co/bookbot/id-g2p-lstm).

## Phoneme and Grapheme Sets

```python
graphemes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
phonemes = ['a', 'b', 'd', 'e', 'f', 'ɡ', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'z', 'ŋ', 'ə', 'ɲ', 'tʃ', 'ʃ', 'dʒ', 'x', 'ʔ']
```

## Implementation Details

You can find more details on how we handled homographs and out-of-vocabulary prediction on our [documentation](https://bookbot-kids.github.io/g2p_id/algorithm/) page.

## References

```bib
@misc{g2pE2019,
  author = {Park, Kyubyong & Kim, Jongseok},
  title = {g2pE},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/Kyubyong/g2p}}
}
```

```bib
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
