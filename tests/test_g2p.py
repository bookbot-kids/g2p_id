def test_g2p(g2p):
    assert g2p("Apel itu berwarna merah.") == [
        ["a", "p", "ə", "l"],
        ["i", "t", "u"],
        ["b", "ə", "r", "w", "a", "r", "n", "a"],
        ["m", "e", "r", "a", "h"],
        ["."],
    ]
    assert g2p("Rahel bersekolah di S M A Jakarta 17.") == [
        ["r", "a", "h", "e", "l"],
        ["b", "ə", "r", "s", "ə", "k", "o", "l", "a", "h"],
        ["d", "i"],
        ["e", "s"],
        ["e", "m"],
        ["a"],
        ["dʒ", "a", "k", "a", "r", "t", "a"],
        ["t", "u", "dʒ", "u", "h"],
        ["b", "ə", "l", "a", "s"],
        ["."],
    ]
    assert g2p("Mereka sedang bermain bola di lapangan.") == [
        ["m", "ə", "r", "e", "k", "a"],
        ["s", "ə", "d", "a", "ŋ"],
        ["b", "ə", "r", "m", "a", "i", "n"],
        ["b", "o", "l", "a"],
        ["d", "i"],
        ["l", "a", "p", "a", "ŋ", "a", "n"],
        ["."],
    ]
    assert g2p("Ini rumahnya Aisyah dan Ceri.") == [
        ["i", "n", "i"],
        ["r", "u", "m", "a", "h", "ɲ", "a"],
        ["a", "ʔ", "i", "ʃ", "a", "h"],
        ["d", "a", "n"],
        ["tʃ", "e", "r", "i"],
        ["."],
    ]
    assert g2p("keset selamat datang") == [
        ["k", "e", "s", "e", "t"],
        ["s", "ə", "l", "a", "m", "a", "t"],
        ["d", "a", "t", "a", "ŋ"],
    ]
    assert g2p("kakak layak") == [["k", "a", "k", "a", "k"], ["l", "a", "j", "a", "k"]]


def test_rule_based_g2p(g2p):
    assert g2p._rule_based_g2p("berakhirnya") == "b e r a x i r ɲ a"
    assert g2p._rule_based_g2p("bermaaf-maafan") == "b e r m a ʔ a f - m a ʔ a f a n"
    assert g2p._rule_based_g2p("kecolongan") == "k e tʃ o l o ŋ a n"
    assert g2p._rule_based_g2p("jayapura") == "dʒ a j a p u r a"
    assert g2p._rule_based_g2p("xenon") == "s e n o n"
    assert g2p._rule_based_g2p("layak") == "l a j a k"


def test_lstm(lstm):
    assert lstm.predict("mengembangkannya") == "məŋəmbaŋkanɲa"
    assert lstm.predict("merdeka") == "mərdeka"
    assert lstm.predict("pecel") == "pətʃəl"
    assert lstm.predict("lele") == "lele"


def test_bert(bert):
    assert bert.predict("mengembangkannya") == "məngəmbangkannya"
    assert bert.predict("merdeka") == "mərdeka"
    assert bert.predict("pecel") == "pəcel"
    assert bert.predict("lele") == "lele"
    assert bert.predict("banyak") == "banyak"


def test_ps(g2p):
    assert g2p("psikologi") == [["s", "i", "k", "o", "l", "o", "ɡ", "i"]]
    assert g2p("psikometri") == [["s", "i", "k", "o", "m", "e", "t", "r", "i"]]
    assert g2p("psikotes") == [["s", "i", "k", "o", "t", "e", "s"]]


def test_sticking_dot(g2p):
    assert g2p("Seniornya Brigadir Jendral A.Yani mengambil alih pimpinan.") == [
        ["s", "ə", "n", "i", "ʔ", "o", "r", "ɲ", "a"],
        ["b", "r", "i", "ɡ", "a", "d", "i", "r"],
        ["dʒ", "ə", "n", "d", "r", "a", "l"],
        ["a"],
        ["j", "a", "n", "i"],
        ["m", "ə", "ŋ", "a", "m", "b", "i", "l"],
        ["a", "l", "i", "h"],
        ["p", "i", "m", "p", "i", "n", "a", "n"],
        ["."],
    ]


def test_onnx_wrapper(bert):
    assert bert.predict("mengembangkannya") == "məngəmbangkannya"
    model_state = bert.model.__getstate__()
    bert.model.__setstate__(model_state)
    assert bert.predict("mengembangkannya") == "məngəmbangkannya"
