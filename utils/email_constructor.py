import base64
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
from pathlib import Path
import pytz
import random

from utils import constants

def load_joke() -> tuple:
    with Path.open(constants.JOKE_CSV_PATH, "r", encoding="utf-8") as f:
        jokes = f.read()
    jokes = jokes.split("\n")
    selected_joke = jokes[random.randint(1,len(jokes)-1)]

    joke = selected_joke.split(",")[0].strip()
    punchline = selected_joke.split(",")[1].strip()
    return joke, punchline

def load_memes() -> tuple:
    list_of_memes = os.listdir(Path.joinpath(Path.cwd(), "meme_vault"))
    list_of_memes.remove("jokes.csv")
    selected_meme = list_of_memes[random.randint(0,len(list_of_memes)-1)]
    with Path.open(Path.joinpath(Path.cwd(), "meme_vault", selected_meme), "rb") as f:
        image = f.read()
    return(selected_meme, image)

def message_builder(sender: str, recipient:list, bcc:str, body:str, images:list):
    message = MIMEMultipart("related")
    message["To"] = ", ".join(recipient)
    message["From"] = sender
    # Generate the date time string for the subject
    date_time_string = datetime.now(pytz.timezone("Europe/London")).strftime("%A %d %B")
    message["Subject"] = constants.EMAIL_SUBJECT.format(date_string=date_time_string)
    
    if bcc:
        message["Bcc"] = ", ".join(bcc)

    # https://stackoverflow.com/questions/920910/sending-multipart-html-emails-which-contain-embedded-images
    msgAlternative = MIMEMultipart("alternative")
    message.attach(msgAlternative)

    msgText = MIMEText('Something must have gone wrong! This email is constructed with HTML not plain text! Please view in a suitable email viewer')
    msgAlternative.attach(msgText)

    # Select a Joke
    msgText = MIMEText(body, "html")

    msgAlternative.attach(msgText)

    # Add each image in the array to the email
    for i in range(0,len(images)):
        msg_image = MIMEImage(images[i])
        msg_image.add_header("Content-ID", f"<image_{str(i)}>")
        message.attach(msg_image)

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return encoded_message