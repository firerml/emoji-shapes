# {shape: (code, min number of emojis, max number of emojis, default emoji)}
SHAPE_CODES = {
    'box': {'min': 0, 'max': 3, 'default': ':thumbsup:', 'code': ['>212\n>101\n>212']},
    'on_the_can': {'min': 0, 'max': 1, 'default': ':rage1:', 'code': ['>0\n>   :toilet:']},
    'thumb': {'min': 0, 'max': 1, 'default': ':thumbsup:', 'code': [
        '> ' +
        '\n>                          00' +
        '\n>                          00' +
        '\n>                        00' +
        '\n>                    00000' +
        '\n>000000000' +
        '\n>000000000' +
        '\n>000000000' +
        '\n>                     0000\n>\n>'
    ]},
    'smile': {'min': 0, 'max': 2, 'default': ':simple_smile:', 'code': [
        '> ' +
        '\n>          0      0' +
        '\n>          0      0' +
        '\n>1                        1' +
        '\n>  1                      1' +
        '\n>    1                  1' +
        '\n>       1111\n>\n>'
    ]}
}
