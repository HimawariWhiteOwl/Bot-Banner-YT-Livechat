import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytchat

VdoId = ""

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
client_secrets_file = "API/client_secret_project_YoutubeApi.json"
liveChatId = None
creds = None

def OAuth(creds):
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
    api_service_name = "youtube"
    api_version = "v3"
    youtubeServices = build(api_service_name, api_version, credentials=creds)
    return youtubeServices
def GetLiveChatChannelId(yts):
    print("Enter Youtube VdoID")
    VdoId = input("Example (https://www.youtube.com/watch?v=VDOID) : ")
    request = yts.liveBroadcasts().list(
        part="snippet",
        id=VdoId
    )
    response = request.execute()
    print(response)
    liveChatId = response["items"][0]["snippet"]["liveChatId"]
    return liveChatId , VdoId

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
    return response
def CaseBan(ms,Status):
    V_index = ms.find("V")
    dot_index = ms.find(".")
    space_index = ms.find(" ")

    if (V_index == 0 and dot_index == 4):
        start = (dot_index + 1) - V_index
        end = len(ms) - space_index
        print("C2 {0} start{1}-end{2}".format(ms, start, end))
        Status = True
    elif (V_index == 0 and space_index == 4):
        start = (space_index + 1) - V_index
        end = len(ms) - dot_index
        print("C3 {0} start{1}-end{2}".format(ms, start, end))
        Status = True
    elif ("ONLINE" in ms and (ms[space_index + 1] == "." or ms[dot_index + 1] == " ")):
        start = (space_index + 1) - V_index
        end = len(ms) - dot_index
        print("C4 {0} start{1}-end{2}".format(ms, start, end))
        Status = True
    return Status
def YoutubeBanUser(youtube,liveChatId,spamYTchannelId):
    request = youtube.liveChatBans().insert(
        part="snippet",
        body={
            "snippet": {
                "liveChatId": liveChatId,
                "type": "permanent",
                "bannedUserDetails": {
                    "channelId": spamYTchannelId
                }
            }
        }
    )
    response = request.execute()
    print(response)

def main():
    liveChatId = None
    Status = False
    while(True):
        youtubeServices = OAuth(creds)
        if liveChatId == None:
            liveChatId,VdoId = GetLiveChatChannelId(youtubeServices)
        else:
            chat = pytchat.create(video_id=VdoId)
            while chat.is_alive():
                try:
                    youtubeServices = OAuth(creds)
                    message = chat.get()
                    for c in message.items:
                        print(
                            f"{c.datetime} [{c.author.name}] : "
                            f"{c.message} "
                            f"Link:{c.author.channelUrl} "
                            f"ChannalID:{c.author.channelId}")
                        Status = CaseBan(c.message.upper(),Status)
                        if (Status == True):
                            YoutubeBanUser(youtubeServices, liveChatId, c.author.channelId)
                            response = InsertChat(youtubeServices, liveChatId,
                                       "{0} @{1} Let's Say hello my Bot Banner. Support By @Hoshimura Himawari"
                                                  .format("Bye Bye", c.author.name))
                        Status = False
                except AssertionError as error:
                    print(error)
                    print("Not Working")
                except HttpError as err:
                    print(err)
if __name__ == '__main__':
    main()