def latin_to_cyrillic(input_str: str) -> str:
    """
    заменяет латинские буквы, похожие на кириллические, на соответствующие кириллические.
    """
    if not input_str or not isinstance(input_str, str):
        return input_str
    
    latin_to_cyrillic_map = {
        'A': 'А', 'B': 'В', 'C': 'С', 'E': 'Е', 'K': 'К',
        'M': 'М', 'H': 'Н', 'O': 'О', 'P': 'Р', 'T': 'Т',
        'X': 'Х', 'Y': 'У'
    }
    
    # заменяем символы
    result = ''.join(
        latin_to_cyrillic_map.get(char, char)
        for char in input_str
    )
    
    return result 





