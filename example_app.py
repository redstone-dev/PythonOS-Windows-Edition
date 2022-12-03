import pyos_sdk as sdk

class MainWindow(sdk.PyApplication):
    def __init__(self) -> None:
        self.procname = "Example"
        super().__init__()

    def main(self, /, plugin=None):
        if not plugin:
            print("Mark Zuckerberg is not human")
            input()
        else:
            plugin().main()
        return self

def run():
    MainWindow()

run()