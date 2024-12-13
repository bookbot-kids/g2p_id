import typing
import asyncio 
import logging
import libsql_client
import asyncio 
import time
from typing import Dict, Tuple

from pathlib import Path
from gruut.const import PHONEMES_TYPE
from gruut.phonemize import SqlitePhonemizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

_LOGGER = logging.getLogger(__name__)

async def _fetch_lexicon_from_turso(turso_config) -> Dict[str, str]:
    """Fetches lexicon from Turso database using batching and parallel queries.
    Only fetches non-homographs (where role is empty string).

    Args:
        turso_config: Dictionary containing Turso configuration
            - url: Turso database URL
            - auth_token: Authentication token
            - table: Table name

    Returns:
        Dict[str, str]: Dictionary mapping words to phonemes
    """
    start_time = time.time()
    _LOGGER.info("Starting to fetch lexicon from Turso...")
    
    client = libsql_client.create_client(
        url=turso_config["url"],
        auth_token=turso_config["auth_token"]
    )
    
    try:
        # Get total count first
        count_result = await client.execute(
            f"SELECT COUNT(*) FROM {turso_config['table']} WHERE role = ''"
        )
        total_count = count_result.rows[0][0]
        
        # Initialize batch size
        batch_size = 5000
        
        # Create concurrent tasks for fetching data
        tasks = []
        for offset in range(0, total_count, batch_size):
            query = f"""
                SELECT word, phonemes 
                FROM {turso_config['table']} 
                WHERE role = ''
                LIMIT {batch_size} 
                OFFSET {offset}
            """
            tasks.append(client.execute(query))
        
        # Execute all queries concurrently
        results = await asyncio.gather(*tasks)
        
        # Process results into dictionary
        lexicon = {}
        total_rows = 0
        for result in results:
            rows = result.rows
            if rows:
                total_rows += len(rows)
                for row in rows:
                    lexicon[row[0].lower()] = row[1]
        
        total_time = time.time() - start_time
        _LOGGER.info(f"Loaded {total_rows} lexicon entries in {total_time:.2f} seconds")
        
        return lexicon
        
    finally:
        await client.close()

async def _fetch_homographs_from_turso(turso_config) -> Dict[str, Tuple[str, str, str, str]]:
    """Fetches homographs from Turso database using batching and parallel queries.
    Only fetches rows where role is not empty.

    Args:
        turso_config: Dictionary containing Turso configuration
            - url: Turso database URL
            - auth_token: Authentication token
            - table: Table name

    Returns:
        Dict[str, Tuple[str, str, str, str]]:
            Key: WORD
            Value: (PH1, PH2, POS1, POS2)
    """
    start_time = time.time()
    _LOGGER.info("Starting to fetch homographs from Turso...")
    
    client = libsql_client.create_client(
        url=turso_config["url"],
        auth_token=turso_config["auth_token"]
    )
    try:
        # Get total count first for rows with non-empty roles
        count_result = await client.execute(
            f"SELECT COUNT(*) FROM {turso_config['table']} WHERE role != ''"
        )
        total_count = count_result.rows[0][0]
        # Initialize batch size
        batch_size = 5000
        
        # Create concurrent tasks for fetching data
        tasks = []
        for offset in range(0, total_count, batch_size):
            query = f"""
                SELECT word, phonemes, role
                FROM {turso_config['table']} 
                WHERE role != ''
                ORDER BY word, role  -- Ensure consistent ordering for pairs
                LIMIT {batch_size} 
                OFFSET {offset}
            """
            tasks.append(client.execute(query))
        
        # Execute all queries concurrently
        results = await asyncio.gather(*tasks)
        
        # Process results into dictionary
        homographs = {}
        current_word = None
        current_data = []
        total_pairs = 0
        
        # Process all results
        for result in results:
            for row in result.rows:
                word, phonemes, role = row
                word = word.lower()
                
                if current_word != word:
                    # Store previous word's data if we have a complete pair
                    if len(current_data) == 2:
                        homographs[current_word] = (
                            current_data[0][0],  # ph1
                            current_data[1][0],  # ph2
                            current_data[0][1],  # pos1
                            current_data[1][1]   # pos2
                        )
                        total_pairs += 1
                    # Start new word
                    current_word = word
                    current_data = [(phonemes, role)]
                else:
                    # Add second pronunciation for current word
                    if len(current_data) < 2:
                        current_data.append((phonemes, role))
        
        # Don't forget to process the last word
        if len(current_data) == 2:
            homographs[current_word] = (
                current_data[0][0],  # ph1
                current_data[1][0],  # ph2
                current_data[0][1],  # pos1
                current_data[1][1]   # pos2
            )
            total_pairs += 1
        
        total_time = time.time() - start_time
        _LOGGER.info(f"Loaded {total_pairs} homograph pairs in {total_time:.2f} seconds")
        
        return homographs
        
    finally:
        await client.close()
