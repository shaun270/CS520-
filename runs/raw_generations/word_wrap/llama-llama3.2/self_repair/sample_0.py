def word_wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 > width:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " "
            current_line += word
    
    if current_line:
        lines.append(current_line)
    
    return lines