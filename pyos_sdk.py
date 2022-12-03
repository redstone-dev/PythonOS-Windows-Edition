class PyOSApplication:
    def __init__(self, /, space, user) -> None:
        try:
            self.procname
        except(NameError):
            self.procname = "PythonOS Application"
        
        self.space = space
        if self.space > 1:
            self.user = user
        else:
            self.user = "kernel"
    
    def main(self): return None

class PyOS_Errcode:
    def __init__(self, value) -> None:
        self.value = str(value)

class PyOS_Error:
    def __init__(self, cause: str, /, fatal=False) -> None:
        import sys

        # If there is an error code already defined, define a default one
        try:
            self.errcode
        except(AttributeError):
            self.errcode = PyOS_Errcode(10)
        
        self.cause = cause

        if not fatal:
            print(f"<{self.__class__.__name__}> {cause}")
        else:
            print(f"Fatal error!\n<{self.__class__.__name__}> {cause}")
            sys.exit(1)
            
            
class PyOS_App_Error(PyOS_Error):
    def __init__(self, cause, /, fatal=False) -> None:
        self.errcode = PyOS_Errcode(11)
        super(cause, fatal=fatal)

class PyOS_NoUserSpecified_Error(PyOS_App_Error):
    def __init__(self, cause="No user assigned to this application", /, fatal=True) -> None:
        super(cause, fatal=fatal)

class PyOS_EmptyInput_Error(PyOS_App_Error):
    def __init__(self, cause="Could not process an empty input", /, fatal=False):
        super(cause, fatal=fatal)

def throw(error: PyOS_Error):
    return (error.errcode, error.cause)