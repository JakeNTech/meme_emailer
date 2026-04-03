import os
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from utils import constants

class gmail():
    def __init__(self, refresh_token):
        # Validate the refresh token
        self._validate_refresh_token(refresh_token)
        if self.valid_token:
            creds = Credentials.from_authorized_user_info(refresh_token, constants.SCOPES)
            self.service = build("gmail", "v1", credentials=creds)
        else:
            print("Token is invalid")


    def _validate_refresh_token(self, refresh_token):
        auth = Credentials.from_authorized_user_info(refresh_token, constants.SCOPES)
        # If the credentials aren't valid but because they have expired
        if (auth.valid == False and auth.expired == True and auth.refresh_token):
            auth.refresh(Request())
            os.environ["G_TOKEN"] = auth.to_json()
            self.valid_token = True
        else:
            self.valid_token = False

    def send_email(self, message):
        """Sends the message object from the account.

        returns:
            message object
        """
        try:
            sent_message = (
                self.service.users()
                .messages()
                .send(userId="me", body={"raw": message})
                .execute()
            )
            successful = True
        except Exception as err:
            successful = False
            sent_message = {"error": err}

        return successful, sent_message