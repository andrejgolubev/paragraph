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

if __name__ == "__main__":
    print(latin_to_cyrillic("543м"))
    print(latin_to_cyrillic("543O"))
    print(latin_to_cyrillic("543P"))
    print(latin_to_cyrillic("543T"))
    print(latin_to_cyrillic("543X"))
    print(latin_to_cyrillic("543Y"))



