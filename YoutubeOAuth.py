import os.path
from google_auth_httplib2 import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def OAuth(creds,client_secrets_file,ExitFile,SCOPES):
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time
    if os.path.exists(ExitFile):
        creds = Credentials.from_authorized_user_file(ExitFile, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=3090)
        # Save the credentials for the next run
        with open(ExitFile, 'w') as token:
            token.write(creds.to_json())
    api_service_name = "youtube"
    api_version = "v3"
    youtubeservices = build(api_service_name, api_version, credentials=creds)
    return youtubeservices