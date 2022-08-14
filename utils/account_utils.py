import xmpp

def register_user_account() -> bool:
  email_input = input("Please enter your email: ")
  password_input = input("Please enter your password: ")

  jid = xmpp.JID(email_input)
  account = xmpp.Client(jid.getDomain(), debug=[])
  account.connect()

  response = bool(xmpp.features.register(account, jid.getDomain(), {
            'username': jid.getNode(),
            'password': password_input
  }))

  return response
