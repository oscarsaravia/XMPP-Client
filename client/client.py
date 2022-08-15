import slixmpp
from aioconsole import ainput
from utils import menu_utils

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
        print("STARTING CLIENT...")
        chat_menu = menu_utils.get_chat_interface()
        self.send_presence()
        await self.get_roster()
        online = True
        while online:
            print(chat_menu)
            option_selected = int(input('==> '))
            if (option_selected == 1):
                roster = self.client_roster.groups()
                roster_values = roster.get("")
                for x in range(len(roster_values)):
                    print(x + 1, ': ', roster_values[x])
            elif (option_selected == 2):
                contact_to_add = input("Enter the contact email: ")
                self.send_presence_subscription(pto= contact_to_add)
                print('ADD CONTACT REQUEST SENT!')
                
            elif (option_selected == 3):
                emisor = self.jid + ': '
                receptor = 'oscarsaravia@alumchat.fun'
                keep_chat = True
                print('To exit back to menu, write exit()')
                while keep_chat:
                    message = await ainput(emisor)
                    if message == 'exit()':
                        keep_chat = False
                    self.send_private_message(receptor, message)
            elif (option_selected == 4):
                print()
                contact_selected = await ainput('Contact JID: ')
                roster = self.client_roster.groups()
                contact_list = roster
                # xmpp.contact_list(specific = contact_selected)
            elif (option_selected == 5):
                options = ['chat', 'away', 'xa Available', 'dnd']
                menu_utils.show_presence_options()
                option = await ainput('==> ')
                message_test = 'HOLA MUNDO!'
                if (int(option) >= 1 and int(option) <= 5):
                    presence_value = options[int(option) - 1]
                self.send_presence(pshow=presence_value, pstatus=message_test)
            elif (option_selected == 6):
                self.disconnect(wait=False)
                online = False

    def message(self, msg):
        emisor = str(msg['from'])
        emisor_name = emisor.split('/')[0]
        if msg['type'] in ('chat', 'normal'):
            print(emisor_name, ': %(body)s'% msg)
            # msg.reply("Thanks for sending\n%(body)s" % msg).send()
    
    def send_private_message(self, receptor, message = ''):
	    self.send_message(
			mto=receptor,
			mbody=message,
			mtype='chat'
		)

