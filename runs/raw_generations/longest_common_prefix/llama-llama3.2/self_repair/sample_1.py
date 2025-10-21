def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""
    
    prefix = min(strs, key=len)
    for i, char in enumerate(prefix):
        for other in strs:
            if other[i] != char:
                return prefix[:i]
    return prefix