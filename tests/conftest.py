import pytest
from g2p_id import G2p


@pytest.fixture(scope="session")
def g2p():
    return G2p()
