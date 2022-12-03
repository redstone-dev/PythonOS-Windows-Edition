import pyos_sdk as sdk

class Calculator(sdk.PyOSApplication):
    def __init__(self, /, space=3, user=None):
        self.procname = "Calculator"
        super(space=space, user=user)