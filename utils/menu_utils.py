def get_menu_interface() -> str:
  menu = '''
    ===== WELCOME TO XMPP CLIENT =====\n
    Please enter an option: \n
    1. Register Account
    2. Login
    3. Quit
  '''

  return menu

def get_chat_interface() -> str:
  chat_menu = '''
    === PLEASE, SELECT AN OPTION ===
    1. Show contacts
    2. Add new contact
    3. Send message to user
    4. Get contact info
    5. Change Presence and Status message
    6. Join Chat Group
    7. Delete Account
    8. Logout
  '''

  return chat_menu

def show_presence_options() -> str:
  presence_options = '''
    === PLEASE SELECT AN OPTION ===
    1. Available
    2. Away
    3. Not Available
    4. Bussy
  '''
  print(presence_options)
