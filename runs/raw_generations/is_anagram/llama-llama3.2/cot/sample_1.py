def is_anagram(a: str, b: str) -> bool:
    a = ''.join(e for e in a if e.isalnum()).lower()
    b = ''.join(e for e in b if e.isalnum()).lower()
    return sorted(a) == sorted(b)