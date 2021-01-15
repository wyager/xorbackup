#!python3
import base64
import sys
import glob

def xor(str1,str2):
    return bytes([a^b for (a,b) in zip(str1,str2)])

(first, *others) = glob.glob("./*.shard")
decrypted = base64.b64decode(open(first,'rb').read())
for other in others:
    decrypted = xor(decrypted, base64.b64decode(open(other,'rb').read()))
sys.stdout.buffer.write(decrypted)