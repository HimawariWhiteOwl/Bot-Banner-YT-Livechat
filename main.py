from googleapiclient.errors import HttpError
import pytchat
import json
from YoutubeOAuth import OAuth
from BanCase import CaseBanUser
from youtube_services import GetLiveChatId, InsertChat, YouTubeBanUser
import time
import datetime

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
client_secrets_file = "API/client_secret_project_YoutubeApi-VT-WhiteOwl.json"
ExitFile = 'token.json'
creds = None
liveChatId = None
VdoId = None


if __name__ == '__main__':
    try:
        youTubeServies = OAuth(creds,client_secrets_file,ExitFile,SCOPES)
        print("OAuth Pass")
        while(True):
            if liveChatId == None:
                liveChatId, VdoId = GetLiveChatId(youTubeServies, VdoId)
                print("get livechatid Pass")
            else:
                try:
                    chat = pytchat.create(video_id=VdoId)
                    while chat.is_alive():
                        try:
                            message = chat.get()
                            for c in message.items:
                                print(f"{c.datetime} [{c.author.name}] : {c.message} Link:{c.author.channelUrl} ChannalID:{c.author.channelId}")
                                Status = CaseBanUser(c.message.lower())
                                if (Status == True):
                                    YouTubeBanUser(youTubeServies, liveChatId, c.author.channelId)
                                    InsertChat(youTubeServies, liveChatId,"{0} @{1} Let's Say hello my Bot Banner. Support By @Hoshimura Himawari".format("Bye Bye", c.author.name))
                                    print(response)
                            time.sleep(5)
                        except AssertionError as error:
                            print(error)
                        except HttpError as err:
                            print(err)
                except Exception as e:
                    print(type(e), str(e))
                    print("VdoId {0} Time out".format(VdoId))
                    chat.terminate()
    except AssertionError as error:
        print(error)