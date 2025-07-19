import base64
import os
import json
import random

# Email bits
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# Google API Bodge
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def gmail_send_mail(creds, to_email, from_email, bcc_email, subject):
	# https://developers.google.com/workspace/gmail/api/guides/sending#python	
	try:
		service = build("gmail", "v1", credentials=creds)
		# message = EmailMessage()
		# message.set_content(contents)
		message = MIMEMultipart("related")
		message["To"] = to_email # To Do: See if this can take a list
		message["From"] = from_email
		message["Bcc"] = bcc_email
		message["Subject"] = subject


		# https://stackoverflow.com/questions/920910/sending-multipart-html-emails-which-contain-embedded-images
		msgAlternative = MIMEMultipart("alternative")
		message.attach(msgAlternative)
		
		msgText = MIMEText('This is the alternative plain text message.')
		msgAlternative.attach(msgText)

		msgText = MIMEText("<p>Todays Meme:</p><br><img src=\"cid:meme\">", "html")
		msgAlternative.attach(msgText)

		# Select Meme
		list_of_memes = os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "memes"))
		selected_meme_path = list_of_memes[random.randint(0,len(list_of_memes)-1)]
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "memes", selected_meme_path), "rb") as f:
			msg_image = MIMEImage(f.read())
		msg_image.add_header("Content-ID", "<meme>")
		message.attach(msg_image)

		# Encode Message
		encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
		# encoded_message = base64.b64encode(message.as_bytes()).decode()

		# Send Message
		create_message = {"raw": encoded_message}
		send_message = (
			service.users()
			.messages()
			.send(userId="me", body=create_message)
			.execute()
		)

		to_return = send_message
		sent = True
	except Exception as e:
		to_return = e
		sent = False
	return(sent ,to_return)

if __name__ == "__main__":
	print("Send a Meme!")
	# Get Creds - https://developers.google.com/people/quickstart/python
	# Bodge for error about defualt creds - > https://stackoverflow.com/questions/35159967/setting-google-application-credentials-for-bigquery-python-cli
	os.environ["GOOGLE_APPLICATION_CREDENTIALS_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "credentials.json")	
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if (os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),"token.json"))):
		creds = Credentials.from_authorized_user_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),"token.json"), SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if ((creds == None) or (not creds.valid)):
		if (creds and creds.expired and creds.refresh_token):
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),"credentials.json"), SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"token.json"), "w") as token:
			token.write(creds.to_json())

	# Open the config file
	if (os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json"))):
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json"), "r") as f:
			config = json.load(f)
	else:
		print("Config file doesn't exist! Will Exit!")
		exit()
	
	# Create email Class
	# Send email
	email_subject = config["subject"] + " " + str(config["subject_ticker"])
	sent, sent_mail = gmail_send_mail(
		creds=creds,
		to_email=config["from"],
		from_email=config["from"],
		bcc_email=",".join(config["recipients"]),
		subject=email_subject,
	)
	# Did it work?
	if (sent == True):
		print(f"Sent mail! ID {sent_mail['id']}")
		# If it did Increment counter
		config["subject_ticker"] = config["subject_ticker"] + 1
		# Re-write the json file
		with open(os.path.join(os.getcwd(),"config.json"), "w") as f:
			json.dump(config, f)
	else:
		print("Error Sending mail!")
		print(sent_mail)