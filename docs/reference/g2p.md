# G2p

::: g2p_id.g2p.G2p

## Usage

```py
texts = [
    "Apel itu berwarna merah.",
    "Rahel bersekolah di Jakarta.",
    "Mereka sedang bermain bola di lapangan.",
]
g2p = G2p(model_type="BERT")
for text in texts:
    print(g2p(text))
```

```py
>> [['a', 'p', 'ə', 'l'], ['i', 't', 'u'], ['b', 'ə', 'r', 'w', 'a', 'r', 'n', 'a'], ['m', 'e', 'r', 'a', 'h'], ['.']]
>> [['r', 'a', 'h', 'e', 'l'], ['b', 'ə', 'r', 's', 'ə', 'k', 'o', 'l', 'a', 'h'], ['d', 'i'], ['dʒ', 'a', 'k', 'a', 'r', 't', 'a'], ['.']]
>> [['m', 'ə', 'r', 'e', 'k', 'a'], ['s', 'ə', 'd', 'a', 'ŋ'], ['b', 'ə', 'r', 'm', 'a', 'i', 'n'], ['b', 'o', 'l', 'a'], ['d', 'i'], ['l', 'a', 'p', 'a', 'ŋ', 'a', 'n'], ['.']]
```