from flask import Flask, Response, request

app = Flask(__name__)


def _shapes():
    return {
        'box': (lambda emoji: ((emoji*3 + '\n')*3)[:-1])
    }


def make_shape(shape_name, emoji):
    func = _shapes().get(shape_name)
    if func:
        return func(emoji)
    return ''


@app.route('/', methods=['GET'])
def index():
    return "Hello, world."


@app.route('/get_shape', methods=['POST'])
def get_shape():
    text_words = request.form['text'].split(' ')
    shape = text_words[0]
    result = make_shape(shape, text_words[1])
    if not result:
        return 'BAD'
    return Response(result, mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True)
