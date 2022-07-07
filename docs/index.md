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
