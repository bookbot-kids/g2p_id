# Home

## g2p ID: Indonesian Grapheme-to-Phoneme Converter

<p align="center">
    <a href="https://github.com/bookbot-kids/g2p_id/blob/main/LICENSE.md">
        <img alt="GitHub" src="https://img.shields.io/github/license/bookbot-kids/g2p_id.svg?color=blue">
    </a>
    <a href="https://bookbot-kids.github.io/g2p_id/">
        <img alt="Documentation" src="https://img.shields.io/website/http/bookbot-kids.github.io/g2p_id.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/bookbot-kids/g2p_id/releases">
        <img alt="GitHub release" src="https://img.shields.io/github/release/bookbot-kids/g2p_id.svg">
    </a>
    <a href="https://github.com/bookbot-kids/g2p_id/blob/main/CODE_OF_CONDUCT.md">
        <img alt="Contributor Covenant" src="https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg">
    </a>
    <a href="https://github.com/bookbot-kids/g2p_id/actions/workflows/tests.yml">
        <img alt="Tests" src="https://github.com/bookbot-kids/g2p_id/actions/workflows/tests.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/bookbot-kids/g2p_id">
        <img alt="Code Coverage" src="https://img.shields.io/codecov/c/github/bookbot-kids/g2p_id">
    </a>
    <a href="https://discord.gg/gqwTPyPxa6">
        <img alt="chat on Discord" src="https://img.shields.io/discord/1001447685645148169?logo=discord">
    </a>
    <a href="https://github.com/bookbot-kids/g2p_id/blob/main/CONTRIBUTING.md">
        <img alt="contributing guidelines" src="https://img.shields.io/badge/contributing-guidelines-brightgreen">
    </a>
</p>

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