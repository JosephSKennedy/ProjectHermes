from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def main():
	return "Welcome to Court Hack 2017"

@app.route("/voice", methods=['GET','POST'])
def voiceIncoming():
	"""Respond to incoming requests."""
	response = VoiceResponse()
	response.say("Hello Monkey")
	#reponse.hangup()

	return str(response)



if __name__ == "__main__":
	app.run()
	
