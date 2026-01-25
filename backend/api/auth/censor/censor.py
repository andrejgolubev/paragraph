from functools import lru_cache
from pathlib import Path
import re
from backend.api.logger import log

BASE_DIR = Path(__file__).parent.parent.parent.parent

CURSIVE_WORDS_PATH = BASE_DIR / 'api' / 'auth' / 'censor' / 'names-list' / 'cursive_words.txt'

ALLOWED_WORDS_PATHS: list[Path] = [
    BASE_DIR / 'api' / 'auth' / 'censor' / 'names-list' / 'male_names_rus.txt',
    BASE_DIR / 'api' / 'auth' / 'censor' / 'names-list' / 'female_names_rus.txt',
    BASE_DIR / 'api' / 'auth' / 'censor' / 'names-list' / 'male_surnames_rus.txt',
]

TEST_WORDS_PATH = BASE_DIR / 'api' / 'auth' / 'censor' / 'names-list' / 'test.txt'

TOKEN_RE = re.compile(r"[а-яёa-z]+", re.IGNORECASE)


def _tokenize(text: str) -> tuple[str, ...]:
    return tuple(match.group(0) for match in TOKEN_RE.finditer(text))


def levenstein_distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            insert, delete, replace = (
                previous_row[j] + 1,
                current_row[j - 1] + 1,
                previous_row[j - 1],
            )
            if a[j - 1] != b[i - 1]:
                replace += 1
            current_row[j] = min(insert, delete, replace)

    return current_row[n]


def normalize_text(text: str) -> str:
    result = text.replace("-", "").replace(".", "").lower()
    result = re.sub(r"(.)\1{2,}", r"\1", result)
    result = re.sub(r"(.)\1+", r"\1", result)
    return result


def _make_words_loader(normalize: bool = False):
    def _normalizer(line: str) -> str:
        if not (word := line.strip().lower()):
            return ""
        return normalize_text(word) if normalize else word

    @lru_cache(maxsize=512)
    def _load_words(filepath: str) -> tuple[str, ...]:
        with open(filepath, "r", encoding="utf-8") as file:
            return tuple(
                normalized_word
                for line in file
                if (normalized_word := _normalizer(line))
            )

    return _load_words


load_cursive_words = _make_words_loader(normalize=False)
load_allowed_words = _make_words_loader(normalize=True)

ALLOWED_WORDS_SET = frozenset(
    word
    for path in ALLOWED_WORDS_PATHS
    for word in load_allowed_words(path)
)


async def has_cursive_words(
    phrase: str,
    cursive_words_path: str = CURSIVE_WORDS_PATH,
    temperature: float = 0.24,
) -> bool:
    """ 
    параметры:
        phrase: фраза для проверки
        cursive_words_path: путь к текстовому файлу с нецензурными словами, с которыми будет сравнение phrase
        temperature: коэффициент допуска при сравнении ( от 0.0 до 1.0 )
                    например: temperature=0.3 означает, что допускается
                    30% отличий от слова.
    
    возвращает:
        bool: True если найдено нецензурное слово, иначе False
    """

    if not (normalized_phrase:=normalize_text(phrase)):
        return False

    tokens = _tokenize(normalized_phrase)
    log.debug('tokens: %s', tokens)
    if tokens and all(token in ALLOWED_WORDS_SET for token in tokens):
        log.debug("Фраза '%s' полностью в whitelist", normalized_phrase)
        return False

    for word in load_cursive_words(cursive_words_path):
        max_distance = len(word) * temperature
        window = len(normalized_phrase) - len(word) + 1
        if window <= 0:
            continue

        for part in range(window):
            fragment = normalized_phrase[part : part + len(word)]
            if not fragment or fragment in ALLOWED_WORDS_SET:
                continue
            if levenstein_distance(fragment, word) <= max_distance:
                log.debug("Слово %s похоже на %s", phrase, fragment)
                return True
    return False









