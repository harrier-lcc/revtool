import pwn
from pwn import log
import sys
from .strings_util import strings as strings_fn

class Project():
    def __init__(self, path):
        self.path = path
        self.pwntools_binary = pwn.elf.ELF(path)
        with open(path, 'rb') as f:
            self.raw_bytes = f.read()

    def entry(self):
        return self.pwntools_binary.entry

    def strings(self):
        """A very inefficient strings implementation. Not recommand to be used."""
        return strings_fn(self.raw_bytes)

    def start_local(self, args=[]):
        log.debug("start_local")
        argv = [self.path, *args]
        self.io = pwn.gdb.debug(argv, api=True)


    def start_remote(self, host, port, args=[]):
        log.debug("start_remote", host, port)
        pass

    def start(self, args=[]):
        if len(sys.argv) >= 3:
            host = sys.argv[1]
            assert sys.argv[2].isdigit(), "port must be digit"
            port = int(sys.argv[2])
            return self.start_remote(host, port, args=args)
        else:
            return self.start_local(args=args)
