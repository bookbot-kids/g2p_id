import pytest
from g2p_id import G2p, LSTM, BERT


@pytest.fixture(scope="session")
def g2p():
    return G2p()


@pytest.fixture(scope="session")
def lstm():
    return LSTM()


@pytest.fixture(scope="session")
def bert():
    return BERT()
