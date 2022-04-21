# g2p ID: Indonesian Grapheme-to-Phoneme Converter

This library is developed to convert Indonesian graphemes (words) to phonemes in IPA. We followed the methods and designs used in the English equivalent library, [g2p](https://github.com/Kyubyong/g2p).

## Installation

```bash
git clone https://github.com/w11wo/g2p_id.git
cd g2p_id
pip install .
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

This is highly borrowed from the English [g2p](https://github.com/Kyubyong/g2p).

1. Spells out arabic numbers and some currency symbols, e.g. `Rp 200.000 -> dua ratus ribu rupiah`. This is borrowed from [Cahya's code](https://github.com/cahya-wirawan/text_processor).
2. Attempts to retrieve the correct pronunciation for heteronyms based on their POS (part-of-speech) tags.
3. Looks up a lexicon (pronunciation dictionary) for non-homographs. This list is originally from [ipa-dict](https://github.com/open-dict-data/ipa-dict/blob/master/data/ma.txt), and we later made a [modified version](https://huggingface.co/datasets/bookbot/id_word2phoneme).
4. For OOVs, we predict their pronunciations using our [LSTM model](https://huggingface.co/bookbot/id-g2p-lstm).

## Notes

### Homographs

Indonesian words (as far as we know) only has one case of homograph, that is, differing ways to pronounce the letter `e`. For instance, in the word `apel` (meaning: apple), the letter `e` is a mid central vowel `ə`. On the other hand, the letter `e` in the word `apel` (meaning: going to a significant other's house; courting), is a closed-mid front unrounded vowel `e`. Sometimes, a word might have >1 `e`s pronounced in both ways, for instance, `mereka` (meaning: they) is pronounced as `məreka`. Because of this, there needs a way to disambiguate homographs, and in our case, we used their POS (part-of-speech) tags. However, this is not a foolproof method since homographs may even have the same POS tag. We are considering a contextual model to handle this better.

### Attempts that Failed

- Parsed [online PDF KBBI](https://oldi.lipi.go.id/public/Kamus%20Indonesia.pdf), but it turns out that it has very little phoneme descriptions.
- Scraped [online Web KBBI](https://github.com/laymonage/kbbi-python), but it had a daily bandwidth which was too low to be used at this level.

For these, we suggest: [this](https://www.youtube.com/shorts/13ViHuJzP3g).

### Potential Improvements

There is a ton of room for improvements, both from the technical and the linguistic side of the approaches. Consider that a failure of one component may cascade to an incorrect conclusion. For instance, an incorrect POS tag can lead to the wrong phoneme, ditto for incorrect LSTM prediction. We propose the following future improvements.

- [ ] Use a larger pronunciation lexicon instead of having to guess.
- [ ] Find a larger homograph list.
- [ ] Retrain LSTM model with embeddings.
- [ ] Use GRUs instead of LSTM.
- [ ] Use contextual model instead of character-level RNNs.

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
