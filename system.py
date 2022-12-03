import syslib
import sysprg

__boot__ = syslib.BootLoader()
systemuser = __boot__.boot(options=[":clboot", ":loginsu"])

term = sysprg.Terminal(space=2, user=systemuser)
term.main()