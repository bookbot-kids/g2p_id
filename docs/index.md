# Home

## g2p ID: Indonesian Grapheme-to-Phoneme Converter

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
    "Rahel bersekolah di Jakarta.",
    "Mereka sedang bermain bola di lapangan.",
]

g2p = G2p()
for text in texts:
    print(g2p(text))

>> [['a', 'p', 'ə', 'l'], ['i', 't', 'u'], ['b', 'ə', 'r', 'w', 'a', 'r', 'n', 'a'], ['m', 'e', 'r', 'a', 'h'], ['.']]
>> [['r', 'a', 'h', 'e', 'l'], ['b', 'ə', 'r', 's', 'ə', 'k', 'o', 'l', 'a', 'h'], ['d', 'i'], ['dʒ', 'a', 'k', 'a', 'r', 't', 'a'], ['.']]
>> [['m', 'ə', 'r', 'e', 'k', 'a'], ['s', 'ə', 'd', 'a', 'ŋ'], ['b', 'ə', 'r', 'm', 'a', 'i', 'n'], ['b', 'o', 'l', 'a'], ['d', 'i'], ['l', 'a', 'p', 'a', 'ŋ', 'a', 'n'], ['.']]
```

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