
from bbfreeze import Freezer
from sx.system import System
system = System()

include = (
    "sx",
    '__future__',
    #'rpm',
    'os',
    'sys',
    'distutils',
    'docopt',
    'time',
    'logging',
    'subprocess',
    'pipes',
    'platform',
    'webbrowser',
    'socket',
    're',
)
f = Freezer("merlin.%s" % system.arch , includes=include)
f.addScript("merlin.py")
f.addModule('rpm')
f()
