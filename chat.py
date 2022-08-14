from utils import account_utils, menu_utils

execute_menu = True
option_selected = 0
menu = menu_utils.get_menu_interface()

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
    print('LOGIN...')
  elif (option_selected == 3):
    execute_menu = False



