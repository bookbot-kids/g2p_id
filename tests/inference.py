import os
import libsql_client
from g2p_id import G2p

TURSO_URL = os.getenv("TURSO_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

id_turso_config = {
    "url": TURSO_URL,
    "auth_token": TURSO_AUTH_TOKEN,
    "table": "id_phonemes"
}


texts = [
    "Apel itu berwarna merah.",
    "Rahel bersekolah di S M A Jakarta 17.",
    "Mereka sedang bermain bola di lapangan.",
]

g2p = G2p(turso_config=id_turso_config)
for text in texts:
    print(g2p(text))