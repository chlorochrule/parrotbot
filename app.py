#-*- coding: utf-8 -*-

import os
import tweepy
import oauth2 as oauth
from bottle import get, request, redirect, run

request_token_url = 'https://twitter.com/oauth/request_token'
access_token_url = 'https://twitter.com/oauth/access_token'
authenticate_url = 'https://twitter.com/oauth/authenticate'

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']

def get_oauth():
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    client = oauth.Client(consumer)
    resp, content = client.request(request_token_url, 'GET')
    request_token = parse_qsl(content)
    oauth_token = request_token['oauth_token']
    oauth_token_secret = request_token['oauth_token_secret']
    url = '{}?oauth_token={}'.format(authenticate_url, oauth_token)
    os.environ['oauth_token_tmp'] = oauth_token
    os.environ['oauth_token_secret_tmp'] = oauth_token_secret
    return url, oauth_token, oauth_token_secret

@get('/auth')
def authenticate():
    url = get_oauth()[0]
    redirect(url)

@get('/callback')
def callback():
    oauth_token = os.environ['oauth_token_tmp']
    os.unsetenv('oauth_token_tmp')
    oauth_token_secret = os.environ['oauth_token_secret_tmp']
    os.unsetenv('oauth_token_secret_tmp')
    oauth_verifier = request.query['oauth_verifier']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.request_token = {
        'oauth_token': oauth_token,
        'oauth_token_secret': oauth_token_secret,
        'oauth_callback_confirmed': True,
    }
    access_token_key, access_token_secret = auth.get_access_token(oauth_verifier)
    print(access_token_key)
    print(access_token_secret)
    return 'called back'

def parse_qsl(content):
    param = {}
    content = content.decode('utf-8')
    for i in content.split('&'):
        _p = i.split('=')
        param[_p[0]] = _p[1]
    return param

if __name__ == '__main__':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
