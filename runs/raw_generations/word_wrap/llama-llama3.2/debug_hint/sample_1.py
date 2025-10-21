def word_wrap(text: str, width: int) -> list[str]:
    if not text or width < 1:
        return []
    
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(word) > width:
            if current_line:
                lines.append(current_line)
            current_line = word
        elif len(current_line) + (1 if current_line else 0) + len(word) <= width:
            if current_line:
                current_line += " "
            current_line += word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines