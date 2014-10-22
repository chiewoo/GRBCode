class Log:
    def __init__(self, stdout, logpath):
        self.stdout = stdout
        self.logfile = open(logpath, 'w')
    def write(self, s):
        self.stdout.write(s)
        self.logfile.write(s)
#    def close(self):
#        self.logfile.close()

import sys
sys.stdout = Log(sys.stdout, '/tmp/stdout.log')

print 'Hello'
print 1
