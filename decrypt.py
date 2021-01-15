#!python3
import base64
import sys

secret1 = base64.b64decode(open("first_secret.txt",'rb').read())
secret2 = base64.b64decode(open("second_secret.txt",'rb').read())
sys.stdout.buffer.write(bytes(a ^ b for (a,b) in zip(secret1,secret2)))