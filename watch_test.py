from remote_object import Watcher

def ret():
    print "yay"
    
giles = Watcher(ret)

while True:
    pass
