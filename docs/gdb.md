## Design Document for Dynamic GDB instrumentation

```python
from revtool import *

# this will show all I/O, breakpoint status etc
# context.log_level = 'debug'

# Project is a wrapped gdb ELF object
bin = Project('./path')

# remote connection config
# host = 'localhost'
# port = 1234
# r = bin.remote(host, port)



# this breaks in entrypoint
r = bin.start_local()
# you can also start via
# r = bin.start() # determine from cmd args, python solve.py => start_local, python solve.py localhost 3000 => start_remote
# in remote, all breakpoint function will be replaced with nop

# we set all breakpoint first, before all interactions
bp = r.set_breakpoint(0x400100)
bp2 = r.set_breakpoint(0x400200)

# you can also hook function calls:
r.set_call_hook(0x400300, lambda a, b: print(a, b)) # a, b will be param upon calling convention

# or if you need to ignore calling convention
r.set_call_hook_generic(0x400300, lambda bp: print(bp.regs))

# of course, you can hook this with an decorator on a function
# this will skip the call, execute the hook and run next line
@call_hook_generic(0x400300)
def add(bp):
    bp.rax = bp.rax + bp.rbx


# you could potentially mess with return address as well
@call_hook_generic(0x400300)
def random_jump(bp):
    bp.rip = 0x400500
    # this will move rip to 0x400500 and then continue
    bp.skip()



# breakpoints can be hooked with a function.
# It will call the hook with breakpoint object everytime when the breakpoint is reached
bp.hook(lambda bp: print(bp.register('eax')))


# any function attempts to get information from the bp actually makes gdb continue, and run until a breakpoint is hit.
# if execution is stopped before reaching bp, an exception will be raised
# this is raw command sending to gdb. recieving raw string output from gdb.
res = bp.command("der 0x1234 -l 1")
# res is a string returning after the breakpoint is triggered
# get arbitrary registers
eax = bp.register('eax')

# read 0x80 bytes from [rsp-0x4000]
mem_bytes = bp.memory(bp.rsp - 0x4000, 0x80)

# return the current instructions
inst = bp.current_inst() # mov [rsp-0x10], rax

# you can also skip an breakpoint, e.g. continue when the breakpoint is reached
bp2.skip()

# you can run normal "pwntools" like recv/send code as normal.
# it will hang unless it received such input
r.recvuntil('Enter a number?: ')
# and you can fill the input buffer via normal send operations.
# this allows you to programatically to compute values from breakpoint and use it as input, without the need to interact in gdb instead
payload = f"jm9 {rax}"
r.sendline(payload)


# make I/O back to terminal control
bp.interactive()
```
