import logging
from getpass import getpass
from argparse import ArgumentParser
import asyncio

from utils import account_utils, menu_utils
from client import client

execute_menu = True
option_selected = 0
menu = menu_utils.get_menu_interface()

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == '__main__':
    parser = ArgumentParser(description=client.Client.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')


while execute_menu:
  print(menu)
  option_selected = int(input('===> '))
  if (option_selected == 1):
    print('REGISTERING ACCOUNT...\n ')
    status = account_utils.register_user_account()
    if status:
      print('Succesfully created account!')
    else:
      print('Error while creating your account :(')
  elif (option_selected == 2):
    print('LOGGIN IN...')
    # DESCOMENTAR PARA QUE EL USUARIO INGRESE EL EMAIL Y PASSWORD
    # args.jid = input("Username: ")
    # args.password = getpass("Password: ")
    xmpp = client.Client("oscarregister@alumchat.fun", "1234")
  elif (option_selected == 3):
    execute_menu = False



