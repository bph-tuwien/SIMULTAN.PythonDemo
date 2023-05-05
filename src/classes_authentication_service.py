from import_simultan import *

class Python_AuthenticationService(IAuthenticationService):

    __namespace__ = "new_namespace"

    def Authenticate(self, user_manager, project_file):

        user_name = 'admin'
        password = 'admin'

        sec_str = SecureString()

        for char in password:
            sec_str.AppendChar(char)

        user = user_manager.Authenticate(user_name, sec_str)

        user_manager.CurrentUser = user.Item1
        user_manager.EncryptionKey = user.Item2

        return user.Item1