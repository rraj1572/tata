import jwtoken
import threading

m3ustr = '#EXTM3U    x-tvg-url="http://botallen.live/epg.xml.gz" \n\n'
kodiPropLicenseType = "#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha"


def processTokenChunks(channelList):
    global m3ustr
    kodiPropLicenseUrl = ""
    if not channelList:
        print("Channel List is empty ..Exiting")
        exit(1)
    for channel in channelList:
        ls_session_key = jwtoken.generateJWT(channel['channel_id'], iterative=False)
        if ls_session_key != "":
            licenseUrl = channel['channel_license_url'] + "&ls_session=" + ls_session_key
            kodiPropLicenseUrl = "#KODIPROP:inputstream.adaptive.license_key=" + licenseUrl
        else:
            print("Didn't get license for channel: Id: {0} Name:{1}".format(channel['channel_id'],
                                                                            channel['channel_name']))
            print('Continuing...Please get license manually for channel :', channel['channel_name'])
        m3ustr += "#EXTINF:-1  " + "tvg-id=ts" + channel['channel_id'] + "  tvg-logo=" + channel['channel_logo'] + "   group-title=" + channel['channel_genre'] + ",   "
        m3ustr += channel['channel_name'] + "\n" + kodiPropLicenseType + "\n" + kodiPropLicenseUrl + "\n" + channel['channel_url'] + "\n\n"


def m3ugen():
    ts = []
    global m3ustr
    channelList = jwtoken.getUserChannelSubscribedList()
    for i in range(0, len(channelList), 5):
        t = threading.Thread(target=processTokenChunks, args=([channelList[i:i + 5]]))
        ts.append(t)
        t.start()
    for t in ts:
        t.join()

    print("================================================================")
    print("Found total {0} channels subscribed by user \nSaving them to m3u file".format(len(channelList)))
    print("================================================================")
    saveM3ustringtofile(m3ustr)


def saveM3ustringtofile(m3ustr):
    with open("allChannelPlaylist.m3u", "w") as allChannelPlaylistFile:
        allChannelPlaylistFile.write(m3ustr)


def getPrintNote():
    s = " *****************************************************\n" + "Welcome To TataSky Channel Generation Script\n" + \
        "**********************************************************\n" + \
        "- Using this script you can generate playable links based on the channels you have subscribed to \n" + \
        "- You can always read the README.md file if you don't know how to use the generated file \n" + \
        "- You can login using your password or generate an OTP. You need to enter both the Registered Mobile Number \n" + \
        "\n Caution: This doesn't promote any kind of hacking or compromising anyone's details"

    return s


if __name__ == '__main__':
    m3ugen()
