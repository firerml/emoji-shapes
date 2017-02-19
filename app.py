from flask import Flask, Response, request, jsonify
import requests

from shape_maker import get_list, make_shape, ShapeException

app = Flask(__name__)

RESPONSE_TYPE_IN_CHANNEL = "in_channel"
RESPONSE_TYPE_EPHEMERAL = "ephemeral"


@app.route('/', methods=['GET'])
def index():
    return "Hello, world."


@app.route('/get_shape', methods=['POST'])
def get_shape():
    text_words = request.form['text'].split(' ')
    shape = text_words[0]

    # Show user all possible shapes.
    if shape == 'list':
        result = get_list()
        response_type = RESPONSE_TYPE_EPHEMERAL
    else:
        # Put shape in channel (visible to all users).
        try:
            result = make_shape(shape, text_words[1:])
            response_type = RESPONSE_TYPE_IN_CHANNEL
        # Errors are ephemeral (only shown to user)
        except ShapeException as e:
            result = e.message
            response_type = RESPONSE_TYPE_EPHEMERAL
    if request.args.get('format') == 'text':
        return result
    # Keeps the user's slash command from showing up.
    requests.post(request.form['response_url'], json={'text': result, 'response_type': response_type})
    return Response(status=200)


if __name__ == '__main__':
    app.run()
