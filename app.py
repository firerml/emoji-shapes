import os

from flask import Flask, Response, request, jsonify
import requests

import db
from shape_maker import get_list, make_shape, ShapeException

app = Flask(__name__)

CLIENT_ID = '49173439911.142714893344'
RESPONSE_TYPE_IN_CHANNEL = "in_channel"
RESPONSE_TYPE_EPHEMERAL = "ephemeral"

# AUTH_STATE = os.environ.get('ARTMOJI_OAUTH_STATE', '')
AUTH_STATE = 'MAJKmjG8V5HeavKZ'


@app.route('/oauth', methods=['GET'])
def oauth():
    if not request.args.get('state') == AUTH_STATE:
        return jsonify({'ok': False, 'error': 'OAuth state does not match'})
    return jsonify({'ok': True, 'code': request.args['code']})


@app.route('/get_shape', methods=['POST'])
def get_shape():

    print(request.form)

    user_auth_token = db.get_token_str(request.form['user_id'])

    if not user_auth_token:
        oauth_url = 'https://slack.com/oauth/authorize?client_id={}&scope=chat:write:user&team={}&state={}'
        oauth_url = oauth_url.format(CLIENT_ID, request.form['team_id'], AUTH_STATE)
        print(oauth_url)

        token_code = ''
        return jsonify({
            'text': 'Authorize Artmoji to post on your behalf:\n' + oauth_url,
            'response_type': RESPONSE_TYPE_EPHEMERAL
        })
        # res = requests.get(oauth_url)
        #
        # if res.ok:
        #     res_data = res.json()
        #     if res_data['ok']:
        #         token_code = res_data.get('code')
        # if not token_code:
        #     return Response(status=400)

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

    requests.post('https://slack.com/api/chat.postMessage', json={
        'token': token_code, 'channel': request.form['channel_id'], 'text': result
    })
    # Keeps the user's slash command from showing up.
    # requests.post(request.form['response_url'], json={'text': result, 'response_type': response_type})
    # return Response(status=200)


if __name__ == '__main__':
    app.run()
