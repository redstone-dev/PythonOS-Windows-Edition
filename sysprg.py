from pyos_sdk import PyOSApplication, PyOS_Error, throw
from os import system as shell

class Terminal(PyOSApplication):
    def __init__(self, /, space=3, user=None) -> None:
        # Provide a global 'term' object for use in the terminal
        global term
        term = self
        # Required things
        self.procname = "PythonOS Terminal"
        self.space = space
        self.user = user
        self.sessions = []
        self.lines = []
        self.logs = []

        super().__init__(space=self.space, user=user)
        self.main()
        return None
    
    def cmd_lookup(self, cmd: str, args: str):
        # Args must be comma-separated
        # So we check for that here:
        if args.split(",") == args:
            return throw(PyOS_Error("Argument 'args' must be comma-separated"))
        # It might not be the best check, but it will work in most cases.
        # If the eval() further down the line fails, it's another indicator 
        # that you didnt separate 'args' properly.
        # That's the beauty of the way this is designed :)

        try:
            # Look up a command and return it
            return {
                # Also, use the 'term' global just in case
                ".launch": "term.run_program({0}{1})",
                ".help": "term.help()",
                ".exit": "term.exit()",
                ".restore": "term.restore_session()"
            }[cmd]
        except Exception as e:
            # If this fails it was probably because of a bad command.
            return throw(PyOS_Error(f"Error: {e}", fatal=False))

    def run_program(self, path: str, throw_default_exceptions: bool):
        namespace = path.split(":")[0]
        app_type = path.split(":")[1]   

        if not throw_default_exceptions:
            try:
                eval(f"import {namespace}")
                
                try:
                    a = app_type(space=3, user=self.user)
                except Exception as e:
                    throw(PyOS_Error("An error occurred while launching the application: " + str(e)))
                        
            except(ImportError):
                self.write(f"Error: Failed to import {namespace}, possibly because it doesn't exist")
            except(TypeError):
                self.write(f"Error: Possibly too many args passed to {app_type}")
        
    
    def help(self):
        self.run_program("sysprg:Help")
    
    def write(self, text):
        import datetime
        print(text)
        #nice
        """
        The general format for self.write() and self.log() is:
            <time> [<source>] <text>
        'source' is only included if it's not from the main output
        """
        self.lines.append(f"{datetime.datetime.now()} {text}")
        self.logs.append("...")

    def log(self, content):
        import datetime
        self.lines.append(f"{datetime.datetime.now()} [Logs] {str(content)} (Generated from self.log(), read the logs for more info)")
        self.logs[len(self.lines)] = str(content)
    def evaluate(self, expression):
        if expression.startswith("."):
            split = expression.split(" ")
            command_name = split[0]
            command_args = split[1]

            self.cmd_lookup(command_name)
        else:
            if len(expression) > 0:
                self.write(eval(expression))
            else:
                throw(PyOS_Error("Empty expression not allowed"))
    
    def exit(self):
        # Dump logs
        import sys
        if self.space < 3:
            # Cannot exit if it is the shell
            self.write("Can not exit terminal if it is acting as the shell.")
        else:
            # Save a session
            self.write("Saving session...")
            self.sessions.append({
                "term_output" : self.lines,
                "logs" : self.logs
            })

            # Open file and write logs
            with open("system_support/Terminal.log", 'wt') as log:
                import datetime
                session_saved_time = datetime.datetime.now()
                log.seek(0)
                log.write(f"Output for session saved at {session_saved_time}\n")
                for x, y in (self.logs, self.lines):
                    print(f"{x} {y}")
                log.write("End of dump\n")
            sys.exit(0)
    
    # For overriding for yourself.
    def on_login(self, plugin_path: str) -> None: pass

    # This is the main function
    def main(self) -> int:
        # Show welcome message
        self.write("In this terminal you can type plain Python, and it acts as a REPL, or you can type commands starting with '.' to do other things with PythonOS.")
        cmd = None

        if self.space == 3:
            # If in user space, be able to quit
            try:
                while not cmd == ".exit":
                    # Show an input like: test_user> (type here)
                    cmd = input(f"{self.user}> ")
                    self.evaluate(cmd)
            except(KeyboardInterrupt):
                self.exit()
        else:
            # If acting as shell, do not
            while not cmd == ".shutdown":
                try:
                    cmd = input("> ")
                    self.evaluate(cmd)
                except(KeyboardInterrupt): pass
            
        return 0

class FileViewer(PyOSApplication):
    import os
    def __init__(self, /, space=3, user=None) -> None:
        self.procname = "File Viewer"
        super().__init__(space, user)
        self.main()
    
    def list(dirname: str):
        # From https://www.geeksforgeeks.org/os-walk-python/
        import os
        if __name__ == "__main__":
            for (root,dirs,files) in os.walk(dirname, topdown=True):
                print (root)
                print (dirs)
                print (files)
                print ('--------------------------------')

    def main(self): 
        PyOS_Error("Not implemented yet")
        return "10" # until I finish Terminal

class PkgManager(PyOSApplication):
    def __init__(self, /, space, user) -> None:
        super().__init__(space, user)
        self.main()
    
    def main(self):
        return throw(PyOS_Error("Not implemented yet"))

if __name__ == "__main__":
    shell('python3 system.py')