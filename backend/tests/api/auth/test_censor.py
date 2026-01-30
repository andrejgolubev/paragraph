import pytest
from backend.api.auth.censor.censor import TEST_WORDS_PATH, has_cursive_words, ALLOWED_WORDS_PATHS


@pytest.mark.asyncio
async def test_has_cursive_words(): 
    for path in ALLOWED_WORDS_PATHS: 
        with open(path, 'r', encoding='utf-8') as file: 
            for row in file:
                word = row.strip()
                assert not await has_cursive_words(
                    word
                ), f'"{word}" from "{path.name}" marked as cursive.'


@pytest.mark.asyncio 
async def test_words_from_test_words_path():
    with open(path:=TEST_WORDS_PATH, 'r', encoding='utf-8') as file: 
        for row in file:
            word = row.strip()
            assert not await has_cursive_words(
                word
            ), f'"{word}" from "{path.name}" marked as cursive.'