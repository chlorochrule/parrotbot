#-*- coding: utf-8 -*-

import os
from random import randint
import tweepy
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

def get_auth_api():
    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token_key = os.environ['twitter_access_token']
    access_token_secret = os.environ['twitter_access_secret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth_handler=auth, api_root='/1.1')
    return api

def get_reply_text():
    texts = [
        'r u ok??',
        'oh!',
        'www',
        ':-)',
        'really?',
        'ほーん',
        'まじかwww',
        'ウケるwww',
        'えぇ...(困惑)',
        '...',
        'うんうん！'
    ]
    return texts[randint(0, len(texts)-1)]

def get_carousel_message():
    return TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://example.com/item1.jpg',
                    title='this is menu1',
                    text='description1',
                    actions=[
                        PostbackTemplateAction(
                            label='postback1',
                            text='postback text1',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='message1',
                            text='message text1'
                        ),
                        URITemplateAction(
                            label='uri1',
                            uri='http://example.com/1'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://example.com/item2.jpg',
                    title='this is menu2',
                    text='description2',
                    actions=[
                        PostbackTemplateAction(
                            label='postback2',
                            text='postback text2',
                            data='action=buy&itemid=2'
                        ),
                        MessageTemplateAction(
                            label='message2',
                            text='message text2'
                        ),
                        URITemplateAction(
                            label='uri2',
                            uri='http://example.com/2'
                        )
                    ]
                )
            ]
        )
    )

app = Flask(__name__)
channel_access_token = os.environ['channel_access_token']
channel_access_secret = os.environ['channel_access_secret']
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_access_secret)

twitter_bot_api = get_auth_api()

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'carousel':
        message = get_carousel_message()
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    else:
        reply_text = '長すギィ...' if len(event.message.text) > 140 else get_reply_text()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
        twitter_bot_api.update_status(event.message.text.replace('@', ''))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
