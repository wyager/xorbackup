#!python3
import base64
import sys

shards = [0,1,2,3]
num_required = 3

secret = sys.stdin.buffer.read()

# Iterate over all the different ways to pick n things.
# choose(3,"abcd") = [['a','b','c'],['a','b','d'],['a','c','d'],['b','c','d']]
def choose(n,things):
    if n == 0:
        yield []
    elif len(things) == 0:
        pass
    else:
        for sub in choose(n-1,things[1:]):
            yield [things[0]] + sub
        yield from choose(n, things[1:])

def xor(str1,str2):
    return bytes([a^b for (a,b) in zip(str1,str2)])

shardKeys = {shard : {} for shard in shards}

for (pairName, (firstShard,*otherShards)) in zip("abcdefghijklmnopqrstuvwxyz",choose(num_required,shards)):
    encrypted = secret
    for otherShard in otherShards:
        pad = open("/dev/random","rb").read(len(secret))
        encrypted = xor(pad,encrypted)
        shardKeys[otherShard][pairName] = pad
    shardKeys[firstShard][pairName] = encrypted

for (shardName,shardContents) in shardKeys.items():
    with open("shard%s.txt" % shardName, "w") as shardFile:
        shardFile.write(
"""
This is a single shard of recovery data.
To recover the secret, you need to find %s more shard(s),
and xor the data in this shard with the matching
data in another shard(s). For example, if this shard 
has something like:

Pair Name: c
Partial secret:
LECOhrzf

And the other shard(s) has/have something like:

Pair Name: c
Partial secret:
rTaF/Lw5

and

Pair Name: c
Partial secret:
8hNoCGWS

Then you can calculate:
secret1 = bytes(base64.b64decode("LECOhrzf"))
secret2 = bytes(base64.b64decode("rTaF/Lw5"))
secret3 = bytes(base64.b64decode("8hNoCGWS"))
xor = lambda s1,s2 : bytes([a^b for (a,b) in zip(s1,s2)])
decrypted = xor(secret1,xor(secret2,secret3))

==========================================================

"""
            % (num_required - 1)
            )
        for (pairName,halfSecret) in shardContents.items():
            shardFile.write(
"""
Pair Name: %s
Partial secret:
%s
"""
                % (pairName, base64.b64encode(halfSecret).decode('utf-8'))
                )

