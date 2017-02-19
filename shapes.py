SHAPE_CODES = {
    'box': [2, 1, 2, '\n', 1, 0, 1, '\n', 2, 1, 2],
    'on_the_can': [0, '\n   :toilet:']
}


class ShapeException(Exception):
    def __init__(self, message):
        self.message = message


def make_shape(shape_name, emojis):
    code = SHAPE_CODES.get(shape_name)
    if not code:
        raise ShapeException(
            'Invalid shape "%s". Try ```/shape list``` to see all of the possible shapes)' % shape_name
        )
    if not emojis:
        raise ShapeException('Must provide at least one emoji! Try ```/shape box :thumbsup:```')
    for emoji in emojis:
        if emoji[0] != ':' and emoji[-1] != ':':
            raise ShapeException('Emoji names must have colons around them: ```:thumbsup:```')

    max_index = len(emojis) - 1
    result = ''
    for code_piece in code:
        if isinstance(code_piece, int):
            result += emojis[min(code_piece, max_index)]
        else:
            result += code_piece if isinstance(code_piece, str) else str(code_piece)
    return result
