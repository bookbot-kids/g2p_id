# Text Processor

Text Normalisation or Inverse Normalisation for Indonesian, e.g. 

## Measurements
- "123 kg" -> "seratus dua puluh tiga kilogram"
- "10,5 km lagi kita akan mencapai puncak semeru yang bersuhu 5°C" -> "sepuluh koma lima kilometer lagi kita akan mencapai puncak semeru yang bersuhu lima derajat celsius"

## Currency/Money
- "Harga notebook itu $250 atau sekitar Rp 3,000,000" -> "Harga notebook itu dua ratus lima puluh dollar atau sekitar tiga juta rupiah"

## Dates
- "Pecurian itu terjadi hari minggu kemarin (12/3/2021)" ->
  "Pecurian itu terjadi hari minggu kemarin dua belas Maret dua ribu dua puluh satu "

## Time & Time Zone
- "Kebakaran terjadi di wilayah jakarta sejak pukul 22.30 WITA di 1.000 rumah" ->
  "Kebakaran terjadi di wilayah jakarta sejak pukul dua puluh dua lewat tiga puluh menit Waktu Indonesia Tengah di seribu rumah"

## Usage
```
from text_processor import TextProcessor

tp = TextProcessor()
print(tp.normalize("123 kg"))
```