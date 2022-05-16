def GetLiveChatId(yts,VdoId):
    if(VdoId==None):
        print("Enter Your Youtube VDO ID")
        VdoId = input("Excample (https://www.youtube.com/watch?v=VDOID) : ")
        liveChatId = LivecChatId(yts,VdoId)
    else:
        liveChatId = LivecChatId(yts,VdoId)
    return liveChatId,VdoId
def LivecChatId(yts,VdoId):
    request = yts.liveBroadcasts().list(
        part="snippet",
        id=VdoId
    )
    response = request.execute()
    print(response)
    liveChatId = response["items"][0]["snippet"]["liveChatId"]
    return liveChatId
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
    print(response)
def YouTubeBanUser(youtube,liveChatId,spamYtChannelId):
    request = youtube.liveChatBans().insert(
        part="snippet",
        body={
            "snippet": {
                "liveChatId": liveChatId,
                "type": "permanent",
                "bannedUserDetails": {
                    "channelId": spamYtChannelId
                }
            }
        }
    )
    response = request.execute()
    print(response)