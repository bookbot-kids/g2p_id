"""Tests the online g2p_id with the original g2p_id"""
import logging
import typing
import requests
import os
import logging
import unittest

from tqdm import tqdm
from g2p_id import G2p

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger("gruut").setLevel(logging.INFO) 

TURSO_URL = os.getenv("TURSO_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

id_turso_config = {
    "url": TURSO_URL,
    "auth_token": TURSO_AUTH_TOKEN,
    "table": "id_phonemes"
}

g2p_online = G2p(turso_config=id_turso_config)
g2p_offline = G2p()

def get_phonemes_online(text):
    return g2p_online(text)

def get_phonemes_offline(text):
    return g2p_offline(text)

                
class TestPhonemeFunctions(unittest.TestCase):
    def test_phoneme_functions_english(self):
        logging.info("Testing English language phonemes")
        error_log_path = 'phoneme_comparison_errors.log'
        file_path = '/home/s44504/3b01c699-3670-469b-801f-13880b9cac56/dataset_creation/data/indonesian_book_transcripts.txt'
        
        with open(file_path, 'r') as file, open(error_log_path, 'w') as error_log:
            lines = file.readlines()
            for line_number, line in tqdm(enumerate(lines, start=1), total=len(lines), desc="Indonesia Test Progress"):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                try:
                    online_phonemes = get_phonemes_online(line)
                    offline_phonemes = get_phonemes_offline(line)

                    if online_phonemes != offline_phonemes:
                        # Find the differing segments
                        differences = []
                        for i, (online_seg, offline_seg) in enumerate(zip(online_phonemes, offline_phonemes)):
                            if online_seg != offline_seg:
                                differences.append(f"Word {i}: {online_seg} ≠ {offline_seg}")
                        
                        error_message = f"""Mismatch at line {line_number}:
                        Text: {line}
                        Differences: {' | '.join(differences)}
                        """
                        error_log.write(error_message + "\n")
                        logging.warning(error_message)
                except Exception as e:
                    error_message = f"Error processing line {line_number}: {line}\nError: {str(e)}\n"
                    error_log.write(error_message)
                    logging.error(error_message)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
