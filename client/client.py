import slixmpp
from aioconsole import ainput


class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        online = True
        while online:
            option_selected = int(input('Please, select an option ==> '))
            if (option_selected == 1):
                receptor = 'oscarsaravia@alumchat.fun'
                keep_chat = True
                while keep_chat:
                    message = await ainput('==> ')
                    if message == 'exit':
                        keep_chat = False
                    self.send_private_message(receptor, message)
                    print(message)

    def message(self, msg):
        emisor = str(msg['from'])
        emisor_name = emisor.split('/')[0]
        if msg['type'] in ('chat', 'normal'):
            print(emisor_name, ': %(body)s'% msg)
            # msg.reply("Thanks for sending\n%(body)s" % msg).send()
    
    def send_private_message(self, receptor, message = ''):
		# print(f'Sending message to {to}')
		# print(f'Message: {message}')
	    self.send_message(
			mto=receptor,
			mbody=message,
			mtype='chat'
		)
		# print('Message sent succefully')
