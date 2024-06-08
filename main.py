

import json
import os
from flask import app, request
# confusingly similar name, keep these straight in your head
import requests

FB_MESSAGES_ENDPOINT = "https://graph.facebook.com/v2.6/me/messages"

# good practice: don't keep secrets in files, one day you'll accidentally
# commit it and push it to github and then you'll be sad. in bash:
# $ export FB_ACCESS_TOKEN=my-secret-fb-token
FB_TOKEN = os.environ['FB_ACCESS_TOKEN']


@app.route('/', method="POST")
def chatbot_response():
    data = request.json()  # flasks's request object
    sender_id = data["entry"][0]["messaging"][0]["sender"]["id"]
    send_back_to_fb = {
        "recipient": {
            "id": sender_id,
        },
        "message": "this is a test response message"
    }

    # the big change: use another library to send an HTTP request back to FB
    fb_response = requests.post(FB_MESSAGES_ENDPOINT,
                                params={"access_token": FB_TOKEN},
                                data=json.dumps(send_back_to_fb))

    # handle the response to the subrequest you made
    if not fb_response.ok:
        # log some useful info for yourself, for debugging
        print 'jeepers. %s: %s' % (fb_response.status_code, fb_response.text)

    # always return 200 to Facebook's original POST request so they know you
    # handled their request
    return "OK", 200
