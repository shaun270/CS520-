assert len(lines) == (len(text.split(' ')) + len(text.split('\n')) if text else 0)
assert all(len(line) <= width for line in lines)
assert '\n'.join(lines).strip() == text
assert not any(line.startswith('. ') or line.endswith('.\n') for line in lines)
assert '' in lines if text else None
