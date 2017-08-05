import re
import logging

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

class MessageHandler:
    """Breaks down and stores a received message
        Requirements:   1. Must be fast enough to ensure we are not missing messages.
                        2. Must be able to ensure the integrity of a stored message (make sure the pieces all belong together
                        3. Must NOT be dependent on any other class
                        4. Should be extendable enough to use in any other Twitch chat applications"""

    Username = ""
    Payload = []
    CurrentMessage = []

    log = logging.getLogger('MessageHandler')
    logging.basicConfig()

    def ProcessMessage(self, msg):
        """Processes the raw message off the socket and initializes the message object"""
        try:
            self.Username = re.search(r"\w+", msg).group(0)
        except Exception as e:
            self.Username = ""
            logging.exception("MessageHandler::ProcessMsg() - Error handing username")
            return
        try:
            self.Payload.append(CHAT_MSG.sub("", msg))
        except Exception as e:
            self.Payload = ""
            logging.exception("MessageHandler:ProcessMsg() - Error handling message contents")
            #TODO: Find a way to check if this is an EMOJI and see if it can be processed
            return
        finally:
            self.CurrentMessage = self.Payload.rsplit()

    def CheckIfRelevant(self, relevantArgs, onlyFirst = True):
        """ Check to see if the message we just processed is relevant so we can quickly throw it away if it is not
            relevantArgs should be a list of strings to check against(i.e. relevantArgs = ['!', 'ThunBot_']
            This should not be specific but used more for global identifiers. The '!' argument for a Twitch bot signals 
            the beginning of a command"""
