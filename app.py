import os

from flask import Flask, Response, request, jsonify
import requests

from db import DB
from shape_maker import get_list, make_shape, ShapeException

app = Flask(__name__)

RESPONSE_TYPE_IN_CHANNEL = 'in_channel'
RESPONSE_TYPE_EPHEMERAL = 'ephemeral'

AUTH_STATE = os.environ.get('ARTMOJI_OAUTH_STATE', '')
CLIENT_ID = os.environ.get('ARTMOJI_CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('ARTMOJI_CLIENT_SECRET', '')

ERROR_MESSAGE = 'Oops! There was an error. You can email me at firerml (at) gmail (dot) com to report this bug.'


@app.route('/oauth', methods=['GET'])
def oauth():
    # Request and save user's auth token, which will be used to post on the user's behalf.
    if not request.args.get('state') == AUTH_STATE:
        return Response(ERROR_MESSAGE)
    request.args.get('code')
    res_data = requests.get('https://slack.com/api/oauth.access', params={
        'client_id': '49173439911.142714893344',
        'client_secret': '4a8b3da1505c3d80c6320c675665a6e9',
        'code': request.args.get('code', '')
    }).json()
    success = False
    if res_data['ok']:
        success = DB.add_token(res_data['user_id'], res_data['access_token'])

    if not success:
        return Response(ERROR_MESSAGE)
    return 'Great! You\'ve authorized Artmoji to post on your behalf in {}.\n'.format(res_data['team_name']) +\
           'You can close this page and go back to Slack to post beautiful Artmojis. :)'


@app.route('/get_shape', methods=['POST'])
def get_shape():

    user_auth_token = DB.get_token_str(request.form['user_id'])

    if not user_auth_token:
        oauth_url = 'https://slack.com/oauth/authorize?client_id={}&scope=chat:write:user&team={}&state={}'
        oauth_url = oauth_url.format(CLIENT_ID, request.form['team_id'], AUTH_STATE)
        return jsonify({
            'text': 'Authorize Artmoji to post on your behalf:\n' +
                    '(This will never be used for anything but posting artmojis at your request!)\n' +
                    oauth_url,
            'response_type': RESPONSE_TYPE_EPHEMERAL
        })

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

    if response_type == RESPONSE_TYPE_EPHEMERAL:
        return jsonify({'text': result, 'response_type': response_type})
    else:
        # Post on the user's behalf.
        requests.post('https://slack.com/api/chat.postMessage',
                      data={'token': user_auth_token, 'channel': request.form['channel_id'], 'text': result},
                      headers={'Content-Type': 'application/x-www-form-urlencoded'})

    return Response(status=200)


if __name__ == '__main__':
    app.run()
