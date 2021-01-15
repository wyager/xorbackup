#!python3
import base64
import sys

num_shards = 4

secret = sys.stdin.buffer.read()

def xor(str1,str2):
    return bytes([a^b for (a,b) in zip(str1,str2)])

def shardCombos():
    for shard1 in range(0,num_shards):
        for shard2 in range(shard1+1,num_shards):
            yield (shard1,shard2)

shards = {shard : {} for shard in range(0,num_shards)}

for (pairName, (shard1,shard2)) in zip("abcdefghijklmnop",shardCombos()):
    pad = open("/dev/random","rb").read(len(secret))
    encrypted = xor(pad,secret)
    shards[shard1][pairName] = pad
    shards[shard2][pairName] = encrypted

for (shardName,shardContents) in shards.items():
    with open("shard%s.txt" % shardName, "w") as shardFile:
        shardFile.write(
"""
This is a single shard of recovery data.
To recover the secret, you need to find another shard,
and xor the data in this shard with the matching
data in another shard. For example, if this shard 
has something like:

Pair Name: g
Half secret:
fzQPqbIh

And the other shard has something like:

Pair Name: g
Half secret:
DFFs29dV

Then you can calculate:
secret1 = bytes(base64.b64decode("fzQPqbIh"))
secret2 = bytes(base64.b64decode("DFFs29dV"))
decrypted = bytes([a^b for (a,b) in zip(secret1,secret2)])
"""
            )
        for (pairName,halfSecret) in shardContents.items():
            shardFile.write(
"""
Pair Name: %s
Half secret:
%s
"""
                % (pairName, base64.b64encode(halfSecret).decode('utf-8'))
                )

