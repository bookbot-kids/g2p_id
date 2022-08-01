def test_g2p_id(g2p):
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
