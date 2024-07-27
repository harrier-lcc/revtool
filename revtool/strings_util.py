# This modules contains a extremely inefficient string implementation.
# This is not recommanded to be used

import string

def generate_printable(bs: bytes, offset=0, min_size=4, wordlist=string.printable):
    size = len(bs)
    # how should the string diff
    inc = offset + 1

    # generate strings from offseted file
    # e.g. inc = 2, it will check two variants
    # bs[::2] and bs[1::2]
    for byte_offset in range(inc):
        target_bs = bs[byte_offset::inc]
        cur = ""
        for b in target_bs:
            v = chr(b)
            if v in wordlist:
                cur += v
            else:
                if len(cur) >= min_size:
                    yield cur
                cur = b""

# simple_strings aims to replicate how "strings" work
# returns a dedup sorted list of printable strings appear in bytes that are continuous 
# and longer than 4 char. This can be overwritten via `min_size` parameter.
def simple_strings(bs: bytes, min_len=4, wordlist=string.printable):
    ret = set()
    for s in generate_printable(bs, min_size=min_len, wordlist=wordlist):
        ret.add(s)
    ret = list(ret)
    ret.sort()
    return ret

# enumerate strings via possible search offsets, that is, strings seperated with fixed offset
def strings(bs: bytes, min_search_offset=0, max_search_offset=16, min_len=4, wordlist=string.printable):
    ret = set()
    for offset in range(min_search_offset, max_search_offset):
        for s in generate_printable(bs, offset, min_len, wordlist):
            ret.add(s)
    ret = list(ret)
    ret.sort()
    return ret
        
