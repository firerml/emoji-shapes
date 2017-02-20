from shape_codes import SHAPE_CODES


class ShapeException(Exception):
    def __init__(self, message):
        self.message = message


def make_shape(shape_name, emojis):
    shape_info = SHAPE_CODES.get(shape_name)

    # Validations
    if not shape_info:
        raise ShapeException(
            'Invalid shape "%s". Try `/shape list` to see all of the possible shapes)' % shape_name
        )
    code_frames = shape_info['code']
    min_emoji = shape_info['min']

    if len(emojis) < min_emoji:
        raise ShapeException('Must provide at least {} emoji{}!'.format(min_emoji, 's' if min_emoji > 1 else ''))

    # for emoji in emojis:
    #     if emoji[0] != ':' and emoji[-1] != ':':
    #         raise ShapeException('Emoji names must have colons around them: `:thumbsup:`')

    if not emojis:
        emojis.append(shape_info['default'])

    max_index = len(emojis) - 1
    result = ''
    for code in code_frames:
        for code_piece in code:
            if code_piece.isdigit():
                result += emojis[min(int(code_piece), max_index)]
            else:
                result += code_piece
    return result


def get_list():
    message = '*Shape: Number of emojis to provide*\nExample: `/artmoji box :hamburger: :thumbsup:`\n'
    for shape in sorted(SHAPE_CODES.keys()):
        message += '`' + shape + '`:  '
        min_emoji = SHAPE_CODES[shape]['min']
        max_emoji = SHAPE_CODES[shape]['max']
        if min_emoji == max_emoji:
            message += '{}'.format(min_emoji) + 's' if min_emoji > 1 else ''
        else:
            message += '{}-{}'.format(min_emoji, max_emoji)
        message += '\n'
    return message[:-1]
