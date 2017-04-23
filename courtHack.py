from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, render_template

import requests
import json
import sys
import os

import logging 
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


@app.route("/")
def main():
#	return "Welcome to Joe Kennedy's CourtHack hack!"
	return render_template('index.html')


@app.route("/voice", methods=['GET','POST'])
def voice():
	response = VoiceResponse()
	response.say('Hello, welcome to Joes Court House. Your call might be recorded.')
	#response.dial("+19734070493", timeLimit="10", record="record-from-answer-dual", trim="trim-silence")
	response.record(maxLength="10", action="/recording")
	response.hangup()

	return str(response)


@app.route("/dial", methods=['GET','POST'])
def dial():
	recording_url = request.values.get("RecordingURL", None)
	response = VoiceResponse()

	response.say('You are being recorded.')

	return str(response)


@app.route("/recording", methods=['GET','POST'])
def recording():
	response = VoiceResponse()

	recording_url = request.values.get('RecordingUrl', None)
	#print(recording_url)

	response.say('Please verify this is what you said on your call.')
	response.play(recording_url)
	response.say('Good bye.')

	return str(response)

@app.route("/callback", methods=['POST', 'PUT'])
def callback():
#	response = VoiceReponse()
#	response.say("Helllo Hello hello")
#	return str(response)

	add_ons = json.loads(request.values["AddOns"])

	if 'project_hermes' not in add_ons['results']:
		return 'Add VoiceBase Voice Analysis add-on in Twilio console'

	payload_url = add_ons["results"]["project_hermes"]["payload"][0]["url"]

	account_sid = os.environ.get('TWILIO_ACCOUNT_SID') 
	auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
	resp = requests.get(payload_url, auth=(account_sid, auth_token)).json()

#	print(resp)

	results = resp['results'][0]['results']
	text = results['media']["transcripts"]["text"]
#	transcripts = map(lambda res: res[][0]["transcript"], results)
#	temp = VoiceResponse()
#	temp.say("You hit the callback")

	return  str(results)




if __name__ == "__main__":
	handler = RotatingFileHandler('hermes.log',maxBytes=10000,backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.run()





@app.errorhandler(404)
def page_not_found(e):
	app.logger.error(str(e))
	return
