# G2p

::: g2p_id.g2p.G2p

## Usage

```py
texts = [
    "Ia menyayangi yang lain.",
    "Mereka sedang bermain bola di lapangan.",
    "Hey kamu yang di sana!",
    "Rahel pergi ke sekolah dan bertemu dengan Budi.",
]
g2p = G2p(model_type="BERT")
for text in texts:
    print(g2p(text))
```
