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
    command_words = request.form['command'].split(' ')
    print(request.form)
    print(request.form['command'])
    print(command_words)
    shape = command_words[1]
    result = make_shape(shape, command_words[2])
    if not result:
        return 'BAD'
    return Response(result, mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True)
