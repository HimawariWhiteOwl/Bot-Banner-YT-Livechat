import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
client_secrets_file = "API/client_secret_project_YoutubeApi.json"

def InsertChat(youtube,liveChatId,messageText):
    request = youtube.liveChatMessages().insert(
        part="snippet",
        body={
            "snippet": {
                "liveChatId": liveChatId,
                "type": "textMessageEvent",
                "textMessageDetails": {
                    "messageText": messageText
                }
            }
        }
    )
    response = request.execute()
    #print(response)
    return response
def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("Refresh token")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=3090)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('youtube', 'v3', credentials=creds)
        response = InsertChat(service, "KicKGFVDSU56OUZKY3BjZWRsR3NZS1hRa29wQRILWXhFOTZVZlNUeFk", "Hello @{0} Welcome to My Channel www 555 999".format("c.author.name"))
        # Call the People API
        print(response)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()