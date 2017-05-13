import cfg
import requests
import DBInterface

class EmoteManager:

    currentEmotes = []
    currentBTTVEmotes = []
    currentChannelEmotes = []

    def ParseTwitch(self):
        twitch = requests.get(cfg.GLOBAL_EMOTE_URL)
        twitch_data = twitch.json()
        emotes = list(twitch_data['emotes'].keys())  # emote is a list of all the emotes
        return emotes

    def ManageGlobalEmotes(self):
        emotes = self.ParseTwitch() # grab the list of emotes
        DBInterface.GetEmoteList(self.currentEmotes)
        # begin by deleting any emotes from the DB that no longer exist
        for oldEmote in self.currentEmotes[:]:
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
            if element['channel'] is None:
                bttvEmotes.append(element['code'])
        return bttvEmotes

    def ManageBTTVEmotes(self):
        bttvEmotes = self.ParseBTTV()
        DBInterface.GetBTTVEmoteList(self.currentBTTVEmotes)
        # delete any emotes from the DB that no longer exist
        for oldEmote in self.currentBTTVEmotes[:]:
            if oldEmote not in bttvEmotes:
                self.currentBTTVEmotes.remove(oldEmote)
                DBInterface.UnregisterBTTVGlobalEmote(oldEmote)
        # add any new emotes
        for newEmote in bttvEmotes:
            if newEmote not in self.currentBTTVEmotes:  # this list and the DB should be synced up since we just populated the list
                self.currentBTTVEmotes.append(newEmote)
                DBInterface.RegisterBTTVGlobalEmote(newEmote)

    def ParseChannel(self, channel):
        specific = requests.get(cfg.CHAN_EMOTE_URL + channel)
        specific_data = specific.json()
        specificDicts = specific_data['emotes']
        specificEmotes = []
        for element in specificDicts:
            specificEmotes.append(element['code'])
        return specificEmotes

    def ManageChannelEmotes(self, channel):
        specificEmotes = self.ParseChannel(channel)
        DBInterface.GetChannelSpecificEmotes(self.currentChannelEmotes, channel)
        for oldEmote in self.currentChannelEmotes[:]:
            if oldEmote not in specificEmotes:
                self.currentChannelEmotes.remove(oldEmote)
                DBInterface.UnregisterChannelEmote(channel, oldEmote)

        for newEmote in specificEmotes:
            if newEmote not in self.currentChannelEmotes:
                self.currentChannelEmotes.append(newEmote)
                DBInterface.RegisterChannelEmote(channel, newEmote)
