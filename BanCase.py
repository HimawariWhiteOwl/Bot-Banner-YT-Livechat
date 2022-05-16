Banemoji = ["🥰💦💌","💞👍💌","👍💌🤪✅"]
BanText = ["sex","porn","child"]



def CaseBanUser(ms):
    # Ban User
    start = 0
    end = 1
    V_index = ms.find("v")
    dot_index = ms.find(".")
    space_index = ms.find(" ")
    Status = False
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
    elif ("online" in ms and (ms[space_index + 1] == "." or ms[dot_index + 1] == " ")):
        start = (space_index + 1) - V_index
        end = len(ms) - dot_index
        print("C4 {0} start{1}-end{2}".format(ms, start, end))
        Status = True
    elif ("site" in ms and (ms[space_index + 1] == "." or ms[dot_index + 1] == " ")):
        start = (space_index + 1) - V_index
        end = len(ms) - dot_index
        print("C5 {0} start{1}-end{2}".format(ms, start, end))
        Status = True
    elif ("today" in ms and (ms[space_index + 1] == "." or ms[dot_index + 1] == " ")):
        start = (space_index + 1) - V_index
        end = len(ms) - dot_index
        print("C6 {0} start{1}-end{2}".format(ms, start, end))
        Status = True

    elif(ms in Banemoji):
        Status = True
    elif(ms in BanText):
        Status = True
    return Status