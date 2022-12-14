import slixmpp
from aioconsole import ainput, aprint
from utils import menu_utils
import asyncio


class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        # OBJECT VARIABLES
        self.private_chat= ''
        self.group_name = ''
        self.actual_room = ''
        # EVENT HANDLERS
        self.add_event_handler("message", self.message)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.groupchat_message)

        # PLUGINS
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0085')
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0045')
        
        # CONNECT 
        self.connect(disable_starttls=True)
        self.process(forever=False)


    async def start(self, event):
        await aprint("STARTING CLIENT...")
        chat_menu = menu_utils.get_chat_interface()
        # SEND INITIAL PRESENCE AND GET ROSTER
        self.send_presence()
        await self.get_roster()
        online = True
        # LOGGED USSER MENU LOOP
        while online:
            await aprint(chat_menu)
            option_selected = await ainput('==> ')
            option_selected = int(option_selected)

            # SHOW CONTACTS
            if (option_selected == 1):
                await self.get_roster()
                roster = self.client_roster.groups()
                roster_values = roster.get("")
                status_dict = {'': 'Available' , 'away': 'Away', 'xa': 'Not available', 'dnd': 'Busy'}
                # SHOW ALL CONTACTS AND THE RESPECTIVE STATE
                for x in range(len(roster_values)):
                    try:
                        roster = list(self.client_roster.presence(roster_values[x]).items())[0][1]
                        presence = status_dict[roster['show']]
                    except:
                        presence = 'Offline'
                    await aprint(x + 1, ': ', roster_values[x], 'Presence: ', presence)

            # ADD NEW CONTACT
            elif (option_selected == 2):
                contact_to_add = await ainput("Enter the contact email: ")
                self.send_presence_subscription(pto= contact_to_add)
                await self.get_roster()

            # PRIVATE CHAT             
            elif (option_selected == 3):
                emisor = self.jid + ': '
                receptor = await ainput('User email: ')
                self.private_chat = receptor
                keep_chat = True
                await aprint('To exit back to menu, write exit()')
                # CHAT LOOP
                while keep_chat:
                    message = await ainput(emisor)
                    if message == 'exit()':
                        self.private_chat = ''
                        keep_chat = False
                    else:
                        self.send_private_message(receptor, message)

            # GET CONTACT INFO
            elif (option_selected == 4):
                roster = self.client_roster.groups()
                roster_values = roster.get("")
                for x in range(len(roster_values)):
                    await aprint(x + 1, ': ', roster_values[x])
                contact_selected = await ainput('Contact number: ')
                try:
                    roster = list(self.client_roster.presence(roster_values[int(contact_selected) - 1]).items())[0][1]
                    status_dict = {'': 'Available' , 'away': 'Away', 'xa': 'Not available', 'dnd': 'Busy'}
                    status = roster['status']
                    presence = status_dict[roster['show']]
                    # SHOW SPECIFIC USER CONTACT INFO
                    await aprint('===== CONTACT INFO =====')
                    await aprint('STATUS: ', status)
                    await aprint('PRESENCE: ', presence)
                except:
                    # HANDLE OFFLINE USER STATUS
                    await aprint(roster_values[int(contact_selected) - 1], ' is Offline')

            # CHANGE PRESENCE AND STATUS MESSAGE
            elif (option_selected == 5):
                options = ['chat', 'away', 'xa', 'dnd']
                menu_utils.show_presence_options()
                option = await ainput('==> ')
                message_test = await ainput('New status message: ')
                # VALIDATE OPTION
                if (int(option) >= 1 and int(option) <= 5):
                    presence_value = options[int(option) - 1]
                self.send_presence(pshow=presence_value, pstatus=message_test)
                await self.get_roster()

            # JOIN CHAT GROUP
            elif (option_selected == 6):
                groupname = await ainput('Please enter the name you want to use: ')
                chat_id = await ainput('Please enter the chat ID: ')
                self.join_chat_group(groupname, chat_id)
                online = True
                await aprint('Send exit() to leave group chat')
                # GROUP CHAT LOOP
                while online:
                    message = await ainput('==> ')
                    if message == 'exit()':
                        online = False
                        self.private_chat = ''
                    else:
                        await self.group_message(message, self.actual_room)

            # DELETE ACCOUNT
            elif (option_selected == 7):
                await self.delete_account()
                await self.get_roster()
                online = False

            # LOGOUT
            elif (option_selected == 8):
                self.disconnect(wait=False)
                online = False
            
    # MESSAGE HANDLER FUNCTION
    async def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            emisor = str(msg['from'])
            emisor_name = emisor.split('/')[0].split('@')[0]
            # NOTIFICATION HANDLER
            if (emisor.split('/')[0] != self.private_chat):
                await aprint('[NOTIFICACION] ', emisor_name)
            else:
                await aprint(emisor_name, ': %(body)s'% msg)
            # msg.reply("Thanks for sending\n%(body)s" % msg).send()

    # GROUP CHAT MESSAGE HANDLER
    async def groupchat_message(self, message):
        if message['type'] == 'groupchat':
            emisor = str(message['from']).split('/')[1]
            body = str(message['body'])
            
            await aprint(emisor, ": ", body)
    
    # SEND MESSAGE TO A GROUP CHAT
    async def group_message(self, message, chat_group):
        self.send_message(mto=chat_group, mbody=message, mtype='groupchat')

    # REMOVE ACCOUNT FUNCTION
    async def delete_account(self):
            confirmation = await ainput('Are you sure you want to delete your account?: \n1. Yes\n2. No\n')
            if (int(confirmation) == 1):
                try:
                    user_id = self.Iq()
                    await aprint(user_id)
                    user_id['type'] = 'set'
                    user_id['from'] = self.boundjid.user
                    user_id['register']['remove'] = True
                    await user_id.send()
                    self.disconnect()
                except:
                    await aprint('An error ocurred')
                    self.disconnect()
            else:
                await self.get_roster()     
    
    # JOIN CHAT GROUP BY ID
    def join_chat_group(self, username, chat_id):
        self.actual_room = chat_id
        self.plugin['xep_0045'].join_muc(chat_id, username, maxhistory=False)
    
    # SEND ONE TO ONE MESSAGE
    def send_private_message(self, receptor, message = ''):
	    self.send_message(
			mto=receptor,
			mbody=message,
			mtype='chat'
		)

