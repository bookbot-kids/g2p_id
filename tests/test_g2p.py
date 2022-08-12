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
        ["a", "i", "ʃ", "a", "h"],
        ["d", "a", "n"],
        ["tʃ", "e", "r", "i"],
        ["."],
    ]


def test_rule_based_g2p(g2p):
    assert g2p._rule_based_g2p("berakhirnya") == "b e r a x i r ɲ a"
    assert g2p._rule_based_g2p("bermaaf-maafan") == "b e r m a ʔ a f - m a ʔ a f a n"
    assert g2p._rule_based_g2p("kecolongan") == "k e tʃ o l o ŋ a n"
    assert g2p._rule_based_g2p("jayapura") == "dʒ a j a p u r a"
    assert g2p._rule_based_g2p("xenon") == "s e n o n"


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


def test_ps(g2p):
    assert g2p("psikologi") == [["s", "i", "k", "o", "l", "o", "ɡ", "i"]]
    assert g2p("psikometri") == [["s", "i", "k", "o", "m", "e", "t", "r", "i"]]
    assert g2p("psikotes") == [["s", "i", "k", "o", "t", "e", "s"]]
