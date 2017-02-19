from shape_codes import SHAPE_CODES


class ShapeException(Exception):
    def __init__(self, message):
        self.message = message


def make_shape(shape_name, emojis):
    code_frames = SHAPE_CODES.get(shape_name)
    if not code_frames:
        raise ShapeException(
            'Invalid shape "%s". Try `/shape list` to see all of the possible shapes)' % shape_name
        )
    if not emojis:
        raise ShapeException('Must provide at least one emoji! Try `/shape box :thumbsup:`')
    for emoji in emojis:
        if emoji[0] != ':' and emoji[-1] != ':':
            raise ShapeException('Emoji names must have colons around them: `:thumbsup:`')

    max_index = len(emojis) - 1
    result = ''
    for code in code_frames:
        for code_piece in code:
            if code_piece.isdigit():
                result += emojis[min(int(code_piece), max_index)]
            else:
                result += code_piece
    return result
