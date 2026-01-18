import asyncio
from string import ascii_letters  # чтобы запустить асинхронную функцию если надо будет дебажить
import aiofiles
import re


FILEPATH = 'api/auth/misc/cursive_words.txt'

def levenstein_distance(a, b):
    "Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # make sure n <= m, to use O(min(n, m)) space
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


# replacement_dict: dict[str, list[str]] = {
#     "а": ["а", "a", "@"],
#     "б": ["б", "6", "b"],
#     "в": ["в", "b", "v"],
#     "г": ["г", "r", "g"],
#     "д": ["д", "d", "g"],
#     "е": ["е", "e"],
#     "ё": ["ё", "e"],
#     "ж": ["ж", "zh", "*"],
#     "з": ["з", "3", "z"],
#     "и": ["и", "u", "i"],
#     "й": ["й", "u", "i"],
#     "к": ["к", "k", "i{", "|{"],
#     "л": ["л", "l", "ji"],
#     "м": ["м", "m"],
#     "н": ["н", "h", "n"],
#     "о": ["о", "o", "0"],
#     "п": ["п", "n", "p"],
#     "р": ["р", "r", "p"],
#     "с": ["с", "c", "s"],
#     "т": ["т", "m", "t"],
#     "у": ["у", "y", "u"],
#     "ф": ["ф", "f"],
#     "х": ["х", "x", "h", "}{"],
#     "ц": ["ц", "c", "u,"],
#     "ч": ["ч", "ch"],
#     "ш": ["ш", "sh"],
#     "щ": ["щ", "sch"],
#     "ь": ["ь", "b"],
#     "ы": ["ы", "bi"],
#     "ъ": ["ъ"],
#     "э": ["э", "e"],
#     "ю": ["ю", "io"],
#     "я": ["я", "ya"],
# }



def normalize_text(text: str) -> str:
    """Нормализует текст: заменяет символы, приводит к нижнему регистру"""
    # result = text.replace("-", "").replace(" ", "").replace('.', '').lower()
    result = text.replace("-", "").replace('.', '').lower()

    # тут убираем любые повторения буквы длиной >= 3 в одну
    result = re.sub(r"(.)\1{2,}", r"\1", result)
    # теперь чистим двойные повторения
    result = re.sub(r"(.)\1+", r"\1", result)

    # for standard_char, variations in replacement_dict.items():
        # for variation in variations:
            # result = result.replace(variation, standard_char)
    return result


async def has_cursive_words(
    phrase: str,
    filepath: str,
    temperature: float = 0.24
) -> bool:
    """ 
    параметры:
        phrase: фраза для проверки
        filepath: путь к текстовому файлу с нецензурными словами, с которыми будет сравнение phrase
        temperature: коэффициент допуска при сравнении ( от 0.0 до 1.0 )
                    например: temperature=0.3 означает, что допускается
                    30% отличий от длины слова.
    
    возвращает:
        bool: True если найдено нецензурное слово, иначе False
    """
    
    normalized_phrase = normalize_text(phrase)

    async with aiofiles.open(filepath, "r", encoding="utf-8") as file:
        async for line in file:
            word = line.strip().lower()
            max_distance = len(word) * temperature

            for part in range(len(normalized_phrase) - len(word) + 1):
                fragment = normalized_phrase[part : part + len(word)]
                # print(f'fragment: {fragment}', f'word: {word}', sep='\n')
                if fragment and levenstein_distance(fragment, word) <= max_distance:
                    # print(f'Найдено {fragment}', f'Похоже на {word}', sep='\n') # для дебага
                    return True
    return False


if __name__ == '__main__': 
    asyncio.run(
        has_cursive_words(
            # phrase='',
            filepath=FILEPATH,
            temperature=0.24
            )
    )


