def test_text_processor(text_processor):
    # URLs
    assert text_processor.normalize("Situs: https://www.google.com") == "Situs: "
    # measurements
    assert (
        text_processor.normalize("123,1 kg")
        == "seratus dua puluh tiga koma satu kilogram"
    )
    assert text_processor.normalize("500 cm") == "lima ratus centimeter"
    # currency/money
    assert text_processor.normalize("$100") == "seratus dollar"
    assert text_processor.normalize("Rp 3,000,000") == "tiga juta rupiah"
    # dates
    assert (
        text_processor.normalize("(17/8/1945)").strip()
        == "tujuh belas Agustus seribu sembilan ratus empat puluh lima"
    )
    assert text_processor.normalize("(1/13)").strip() == "satu Januari"
    # time/time zone
    assert (
        text_processor.normalize("19.45 WIB")
        == "sembilan belas lewat empat puluh lima menit Waktu Indonesia Barat"
    )
    assert (
        text_processor.normalize("19.00 WIB") == "sembilan belas Waktu Indonesia Barat"
    )
    # numerics
    assert text_processor.normalize("105.000") == "seratus lima ribu"
    assert text_processor.normalize("0,5") == "nol koma lima"
