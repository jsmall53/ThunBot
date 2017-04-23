import cfg
import requests
import DBInterface

class EmoteManager:

    currentEmotes = []
    currentBTTVEmotes = []

    def ParseTwitch(self):
        twitch = requests.get(cfg.GLOBAL_EMOTE_URL)
        twitch_data = twitch.json()
        emotes = list(twitch_data['emotes'].keys())  # emote is a list of all the emotes
        return emotes

    def ManageGlobalEmotes(self):
        emotes = self.ParseTwitch() # grab the list of emotes
        DBInterface.GetEmoteList(self.currentEmotes)
        # begin by deleting any emotes from the DB that no longer exist
        for oldEmote in self.currentEmotes:
            if oldEmote not in emotes:
                self.currentEmotes.remove(oldEmote)
                DBInterface.UnregisterUniversalEmote(oldEmote)
        # now add in any new emotes
        for newEmote in emotes:
            if newEmote not in self.currentEmotes:
                self.currentEmotes.append(newEmote)
                DBInterface.RegisterUniversalEmote(newEmote)

    def ParseBTTV(self):
        bttv = requests.get(cfg.BTTV_EMOTE_URL)
        bttv_data = bttv.json()
        bttvDicts = bttv_data['emotes']
        bttvEmotes = []
        for element in bttvDicts:
            bttvEmotes.append(element['code'])
        return bttvEmotes

    def ManageBTTVEmotes(self):
        bttvEmotes = self.ParseBTTV()
        DBInterface.GetBTTVEmoteList(self.currentBTTVEmotes)
        # delete any emotes from the DB that no longer exist
        for oldEmote in self.currentBTTVEmotes:
            if oldEmote not in bttvEmotes:
                self.currentBTTVEmotes.remove(oldEmote)
                DBInterface.UnregisterBTTVGlobalEmote(oldEmote)
        # add any new emotes
        for newEmote in bttvEmotes:
            if newEmote not in self.currentBTTVEmotes:  # this list and the DB should be synced up since we just populated the list
                self.currentBTTVEmotes.append(newEmote)
                DBInterface.RegisterBTTVGlobalEmote(newEmote)

