def test_text_processor(text_processor):
    # measurements
    assert (
        text_processor.normalize("123,1 kg")
        == "seratus dua puluh tiga koma satu kilogram"
    )
    # currency/money
    assert text_processor.normalize("$100") == "seratus dollar"
    assert text_processor.normalize("Rp 3,000,000") == "tiga juta rupiah"
    # dates
    assert (
        text_processor.normalize("(17/8/1945)").strip()
        == "tujuh belas Agustus seribu sembilan ratus empat puluh lima"
    )
    # time/time zone
    assert (
        text_processor.normalize("19.45 WIB")
        == "sembilan belas lewat empat puluh lima menit Waktu Indonesia Barat"
    )
