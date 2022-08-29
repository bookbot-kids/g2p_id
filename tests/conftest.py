import pytest
from g2p_id import G2p, LSTM, BERT, TextProcessor


@pytest.fixture(scope="session")
def g2p():
    return G2p()


@pytest.fixture(scope="session")
def lstm():
    return LSTM()


@pytest.fixture(scope="session")
def bert():
    return BERT()


@pytest.fixture(scope="session")
def text_processor():
    return TextProcessor()
