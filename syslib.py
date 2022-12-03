import os
from pyos_sdk import PyOSApplication, PyOS_Error

SYSENV = {
    "userlogins": {
        "root": ("root", "password")
    },

    "osvdata": {
        "dbver": "0.1.0",
        "nmver": "PythonOS WE {0} 'Wiarton'"#.format(dbver)
    }
}

class Login(PyOSApplication):
    def __init__(self, /, space=2, user="null") -> None:
        self.procname = "Login"
        self.logged_in_users = []
        self.space = space
        super().__init__(space=self.space, user=user)
    
    def main(self):
        self.verify_login(u="root", p="password")
    
    def verify_login(self, /, u, p, dbg=False):
        if dbg:
            self.logged_in_users.append("root")
            return True # Debug only!
        
        if get_login_from_user(u) == p: # NO case insensitivity.
            self.logged_in_users.append(u)
            return True
        
        return False

def get_login_from_user(name):
    return SYSENV["userlogins"][name.lower()][1]

def get_osv(key) -> str:
    if key.lower() == 'nmver':
        return SYSENV["osvdata"]["nmver"].format(SYSENV["osvdata"]["dbver"])
    return SYSENV["osvdata"][key.lower()]

def sboot(bl_obj, /, soptions=":loginsu"):
    print(soptions.split(","))
    bl_obj.boot(options=soptions.split(" "))

def get_class_name_from_type(clname):
    try:
        return clname().__class__.__name__
    except(NameError):
        raise NameError()

class BootLoader:
    def __init__(self):
        import bootconfig
        self.bootconfig = bootconfig
    
    def boot(self, /, options) -> int:
        import os
        if options == None:
            PyOS_Error("Failed to boot! No boot arguments supplied!", fatal=True)
        else:
            # Run Login which is used to verify user & pswd combinations
            login = Login(space=2, user="root")
            if ":loginsu" in options:
                # Login as super-user
                login.verify_login(u="root", p="password")
            else:
                # Otherwise use the 
                if self.bootconfig.default_user:
                    dfuser = self.bootconfig.default_user
                    login.verify_login(u=dfuser[0], p=dfuser[1])
            os.system("cls")
            print(f"""You're in!
            
Welcome to {get_osv('nmver')}, {login.logged_in_users[0]}""")
            return login

if __name__ == "__main__":
    os.system('python3 system.py')